# ADR-0001: Modular Monolith Architecture for AegisSOC v1.0

## Status

Accepted

## Date

2026-07-25

---

# Context

AegisSOC is designed as an enterprise Security Operations Platform
focused on MITRE ATT&CK based threat detection, threat hunting,
SOC assessment, and AI-assisted investigation.

The platform requires:

- Strong module separation
- Easy deployment inside organizations
- Offline operation
- Secure development
- Future scalability

A microservice architecture introduces additional complexity:

- Service discovery
- Network communication overhead
- Distributed debugging
- Increased infrastructure requirements

---

# Decision

AegisSOC v1.0 will use a Modular Monolith architecture.

Each major capability will exist as an independent module:

- Identity Management
- Event Ingestion
- MITRE Engine
- Detection Engine
- Threat Hunting Engine
- AI Engine
- Reporting Engine

Modules will communicate through well-defined internal interfaces.

---

# Benefits

- Easier development
- Easier deployment
- Reduced infrastructure requirements
- Better debugging
- Strong security boundaries
- Future microservice extraction possible

---

# Consequences

The initial version will run as a single application.

Future high-load components may be extracted:

Example:

AI Engine → Independent Service

Threat Hunting Engine → Independent Service

---

# Security Considerations

The architecture must maintain:

- Module isolation
- Access control
- Audit logging
- Secure APIs
- Least privilege principles

---

# Author

AegisSOC Development Team