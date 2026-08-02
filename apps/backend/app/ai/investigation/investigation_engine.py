from app.ai.knowledge.knowledge_engine import KnowledgeEngine
from app.ai.copilot.local_llm import LocalLLM


class InvestigationEngine:


    def __init__(self):

        self.knowledge = KnowledgeEngine()
        self.llm = LocalLLM()



    def investigate(
        self,
        db,
        vulnerability_id: int
    ):


        context = self.knowledge.get_context(
            db,
            vulnerability_id
        )


        prompt = f"""
You are a Senior SOC Incident Response Analyst.

Analyze the following vulnerability context.

==============================
VULNERABILITY CONTEXT
==============================

{context}


Generate a professional SOC investigation report.

Include:

## Executive Summary

## Vulnerability Analysis

## Technical Details

## MITRE ATT&CK Analysis

## Attack Path

## Threat Actor Perspective

## Business Impact

## Detection Opportunities

## Containment Actions

## Eradication Steps

## Recovery Steps

## SOC Analyst Recommendations


Use clear security analyst language.
Return Markdown format.
"""


        report = self.llm.ask(
            prompt
        )


        return {
            "vulnerability_id": vulnerability_id,
            "context": context,
            "investigation_report": report
        }