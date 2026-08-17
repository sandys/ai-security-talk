#!/usr/bin/env python3
"""OWASP pytm model for the workshop RAG + tool agent.

Run examples:
  python 01_Threat_Modeling/rag_agent_tm.py --dfd
  python 01_Threat_Modeling/rag_agent_tm.py --list
  python 01_Threat_Modeling/rag_agent_tm.py --describe LLM
"""
from pytm import TM, Actor, Agent, Boundary, Dataflow, Datastore, LLM, Server


tm = TM("Customer-support RAG agent")
tm.description = "RAG assistant with an external LLM and approval-gated refund tool"
tm.isOrdered = True

public = Boundary("Public / untrusted")
application = Boundary("Application")
restricted = Boundary("Restricted data")
model_vendor = Boundary("External model vendor")
privileged = Boundary("Privileged action")

user = Actor("Customer")
user.inBoundary = public
api = Server("API gateway")
api.inBoundary = application
agent = Agent("Agent orchestrator")
agent.inBoundary = application
policy = Server("Policy enforcement point")
policy.inBoundary = application
vector_store = Datastore("Vector store")
vector_store.inBoundary = restricted
audit_log = Datastore("Redacted audit log")
audit_log.inBoundary = restricted
llm = LLM("External LLM")
llm.inBoundary = model_vendor
approver = Actor("Human approver")
approver.inBoundary = privileged
refund_tool = Server("Refund tool")
refund_tool.inBoundary = privileged

flows = [
    Dataflow(user, api, "Prompt and session context"),
    Dataflow(api, agent, "Authenticated request"),
    Dataflow(agent, vector_store, "Tenant-scoped retrieval query"),
    Dataflow(vector_store, agent, "Chunks, source, trust label"),
    Dataflow(agent, llm, "Minimum-necessary model context"),
    Dataflow(llm, agent, "Untrusted candidate output"),
    Dataflow(agent, policy, "Typed action proposal"),
    Dataflow(policy, approver, "Approval request for high-risk action"),
    Dataflow(approver, policy, "Signed approval decision"),
    Dataflow(policy, refund_tool, "Scoped capability invocation"),
    Dataflow(agent, audit_log, "Redacted decision and trace metadata"),
]

for flow in flows:
    flow.protocol = "HTTPS"
    flow.isEncrypted = True

if __name__ == "__main__":
    tm.process()
