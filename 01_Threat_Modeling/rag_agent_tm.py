#!/usr/bin/env python3
"""OWASP pytm model for the workshop RAG + tool agent.

The model is ordinary Python, so it can be code-reviewed, diffed, and executed
in CI like any other source file.

Command-line examples (run from the toolkit root)::

    python 01_Threat_Modeling/rag_agent_tm.py --dfd        # Graphviz DOT for the data-flow diagram
    python 01_Threat_Modeling/rag_agent_tm.py --seq        # sequence diagram (PlantUML)
    python 01_Threat_Modeling/rag_agent_tm.py --list       # every threat pytm knows about
    python 01_Threat_Modeling/rag_agent_tm.py --describe LLM
    python 01_Threat_Modeling/rag_agent_tm.py --json tm.json

The notebook ``01_pytm_threat_model.ipynb`` imports ``tm`` from this module and
calls ``tm.resolve()`` in-process, so the same model drives both the CLI and
the interactive lab.
"""
from pytm import TM, Actor, Agent, Boundary, Classification, Data, Dataflow, Datastore, LLM, Server

tm = TM("Customer-support RAG agent")
tm.description = "RAG assistant with an external LLM and an approval-gated refund tool"
tm.isOrdered = True

# --- Trust boundaries ---------------------------------------------------------
public = Boundary("Public / untrusted")
application = Boundary("Application")
restricted = Boundary("Restricted data")
model_vendor = Boundary("External model vendor")
privileged = Boundary("Privileged action")

# --- Elements -----------------------------------------------------------------
user = Actor("Customer")
user.inBoundary = public

api = Server("API gateway")
api.inBoundary = application

agent = Agent("Agent orchestrator")
agent.inBoundary = application
agent.usesExternalTools = True          # it can call the refund tool
agent.validatesToolLaunchConfig = False  # <- toggled in the notebook

policy = Server("Policy enforcement point")
policy.inBoundary = application

vector_store = Datastore("Vector store")
vector_store.inBoundary = restricted

audit_log = Datastore("Redacted audit log")
audit_log.inBoundary = restricted

llm = LLM("External LLM")
llm.inBoundary = model_vendor
llm.isThirdParty = True
llm.processesUntrustedInput = True      # customer prompts and retrieved documents
llm.processesPersonalData = True        # support conversations contain PII
llm.hasSystemPrompt = True
llm.hasRAG = True                       # retrieved chunks are added to the context
llm.hasAgentCapabilities = True         # it proposes tool calls
llm.hasAccessToSensitiveSystems = True  # the refund tool moves money
llm.hasContentFiltering = False         # <- toggled in the notebook
llm.controls.implementsPOLP = False     # <- toggled in the notebook (module 03 builds this)

approver = Actor("Human approver")
approver.inBoundary = privileged

refund_tool = Server("Refund tool")
refund_tool.inBoundary = privileged

# --- Data classifications -----------------------------------------------------
customer_pii = Data("Customer PII", classification=Classification.SENSITIVE, isPII=True)
retrieved_chunks = Data("Retrieved chunks with trust labels", classification=Classification.SENSITIVE)
typed_proposal = Data("Typed action proposal", classification=Classification.SENSITIVE)
audit_event = Data("Redacted decision event", classification=Classification.SENSITIVE)

# --- Data flows (order matters for the sequence diagram) ----------------------
flows = [
    Dataflow(user, api, "Prompt and session context", data=customer_pii),
    Dataflow(api, agent, "Authenticated request", data=customer_pii),
    Dataflow(agent, vector_store, "Tenant-scoped retrieval query"),
    Dataflow(vector_store, agent, "Chunks, source, trust label", data=retrieved_chunks),
    Dataflow(agent, llm, "Minimum-necessary model context", data=retrieved_chunks),
    Dataflow(llm, agent, "Untrusted candidate output"),
    Dataflow(agent, policy, "Typed action proposal", data=typed_proposal),
    Dataflow(policy, approver, "Approval request for high-risk action"),
    Dataflow(approver, policy, "Signed approval decision"),
    Dataflow(policy, refund_tool, "Scoped capability invocation"),
    Dataflow(agent, audit_log, "Redacted decision and trace metadata", data=audit_event),
]

for flow in flows:
    flow.protocol = "HTTPS"
    flow.isEncrypted = True

if __name__ == "__main__":
    tm.process()
