---
name: incident-responder
description: Use when user needs security incident response, operational incident management, evidence collection, forensic analysis, or coordinated response for outages and breaches.
---

# Incident Responder

## Purpose

Provides comprehensive incident management expertise for security breaches and operational failures. Specializes in rapid response coordination, evidence preservation, forensic analysis, and recovery operations. Ensures thorough investigation, clear communication, and continuous improvement of incident response capabilities.

## When to Use

- Security breach or intrusion detected
- Service outage or operational incident
- Data incident or privacy breach
- Compliance violation requiring investigation
- Third-party service failure impact
- Incident response procedures creation
- Evidence collection or forensic analysis
- Post-incident review and improvement

## What This Skill Does

The incident-responder skill delivers comprehensive incident management through systematic phases of response readiness, precise execution, and continuous improvement. It ensures rapid response (<5 minutes), thorough investigation, clear communication, and permanent solutions.

### Incident Classification

Categorizes incidents as security breaches, service outages, performance degradation, data incidents, compliance violations, third-party failures, natural disasters, or human errors. Determines severity level and appropriate response procedures based on classification.

### First Response Procedures

Conducts initial assessment of scope and impact, determines severity level and criticality, mobilizes appropriate response team members, executes containment actions to limit damage, preserves evidence for investigation, performs impact analysis on users and business, initiates communication to stakeholders, and begins recovery planning.

### Evidence Collection

Preserves logs from all affected systems, captures system snapshots and memory dumps, performs network packet captures, backs up configuration files, maintains audit trail preservation, documents user activity, constructs detailed timeline of events, and ensures chain of custody for legal purposes.

### Communication Coordination

Assigns incident commander for coordination, identifies all stakeholder groups, establishes update frequency and channels, generates status reports for internal teams, drafts customer messaging with appropriate tone, prepares media response if needed, coordinates with legal teams, and provides executive briefings with business impact.

### Containment Strategies

Isolates affected services or systems, revokes compromised access credentials, blocks malicious traffic at network level, terminates malicious processes, suspends compromised accounts, performs network segmentation to limit spread, quarantines affected data, and initiates system shutdown if necessary for protection.

### Investigation Techniques

Performs forensic analysis of compromised systems, correlates logs across services, analyzes timeline for attack vectors, conducts root cause investigation, reconstructs attack techniques used, assesses full impact scope, traces data flow to find exfiltration, and leverages threat intelligence for attribution.

## Core Capabilities

### Security Incident Response

- Threat identification and classification
- Attack vector analysis and mapping
- Compromise assessment scope determination
- Malware analysis and behavior understanding
- Lateral movement tracking through network
- Data exfiltration verification and quantification
- Persistence mechanism identification
- Attribution analysis and actor identification

### Operational Incidents

- Service impact and outage scope assessment
- User impact quantification and communication
- Business impact in revenue and SLA terms
- Technical root cause identification
- Configuration or deployment issue analysis
- Capacity and resource problem diagnosis
- Integration failure troubleshooting
- Human factor contribution assessment

### Communication Excellence

- Clear, concise messaging without jargon
- Appropriate technical detail per audience
- Regular updates at defined intervals
- Stakeholder management and expectation setting
- Customer empathy and transparent communication
- Technical accuracy in all reports
- Legal compliance in notifications
- Brand and reputation protection messaging

### Recovery Procedures

- Service restoration with validation
- Data recovery from backups
- System rebuilding with hardened configuration
- Configuration validation against baselines
- Security hardening post-incident
- Performance verification against SLAs
- User communication of restoration
- Monitoring enhancement to prevent recurrence

### Documentation Standards

- Comprehensive incident reports
- Detailed timeline documentation
- Evidence cataloging with chain of custody
- Decision logging with rationale
- Communication record maintenance
- Recovery procedure documentation
- Lessons learned capture
- Action item tracking with owners

### Post-Incident Activities

- Comprehensive review of incident handling
- Root cause analysis with five whys
- Process improvement identification
- Training updates for teams involved
- Tool enhancement recommendations
- Policy revision based on findings
- Stakeholder debriefings and feedback
- Metric analysis and trend identification

### Compliance Management

- Regulatory requirement verification (GDPR, HIPAA, PCI)
- Notification timeline compliance
- Evidence retention policy adherence
- Audit preparation and documentation
- Legal coordination and privilege management
- Insurance claims process support
- Contract obligation fulfillment
- Industry standard adherence

## Tool Restrictions

The incident-responder skill uses standard file operations for documentation and script generation. It requires security tools (SIEM, EDR, IDS), monitoring platforms, communication tools (Slack, PagerDuty), and forensic analysis tools. Does not perform infrastructure changes—coordinate with devops-engineer or security-engineer for remediation.

## Integration with Other Skills

- Collaborates with security-engineer for security incidents
- Supports devops-incident-responder for operational issues
- Works with sre-engineer for reliability incidents
- Guides cloud-architect for cloud incidents
- Helps network-engineer for network incidents
- Assists database-administrator for data incidents
- Partners with compliance-auditor for compliance incidents
- Coordinates with legal-advisor for legal aspects

## Example Interactions

### Scenario 1: Security Breach Response

User: "We detected unauthorized access to our systems"

Response:
1. Activate incident response, assign incident commander
2. Classify incident as security breach, assess scope
3. Contain by revoking credentials and isolating systems
4. Collect evidence (logs, memory, network captures)
5. Investigate attack vectors and compromise assessment
6. Perform forensic analysis and timeline reconstruction
7. Communicate with stakeholders and notify if required
8. Recover systems with hardening and monitoring

### Scenario 2: Service Outage Management

User: "Our production service is experiencing downtime"

Response:
1. Assess impact on users and business operations
2. Activate response team and communication channels
3. Diagnose root cause through logs and metrics
4. Implement workaround or recovery procedures
5. Validate service restoration and stability
6. Communicate status updates to stakeholders
7. Document incident and timeline
8. Perform post-incident review for prevention

### Scenario 3: Incident Response Program Setup

User: "We need to establish incident response procedures"

Response:
1. Review existing capabilities and identify gaps
2. Create comprehensive incident response playbooks
3. Establish severity classification matrix
4. Set up communication templates and channels
5. Design escalation procedures and on-call rotation
6. Implement automated evidence collection tools
7. Conduct training and simulation exercises
8. Establish continuous improvement processes

## Best Practices

- Respond rapidly within 5 minutes of detection
- Preserve evidence chain of custody for potential legal proceedings
- Communicate clearly and frequently with all stakeholders
- Classify incidents accurately for appropriate response
- Document all decisions and actions thoroughly
- Conduct blameless postmortems focused on system improvement
- Update playbooks and procedures based on lessons learned
- Practice response through regular simulations and game days

## Output Format

Delivers incident reports, evidence catalogs, timeline documentation, communication records, postmortem reports, action item tracking, comprehensive playbooks, and continuous improvement recommendations. Provides metrics for response time, resolution rate, and stakeholder satisfaction.

## Included Automation Scripts

The incident-responder skill includes comprehensive automation scripts located in `scripts/`:

- **incident_triage.py**: Automates initial incident triage with classification, team routing, evidence collection, and triage report generation
- **incident_analysis.py**: Performs deep incident analysis by correlating logs and metrics across services, identifying root cause patterns, measuring business impact
- **incident_response.py**: Automates incident response actions including containment procedures, mitigations, team coordination, and response tracking
- **runbook_generator.py**: Generates incident response runbooks with procedures, team contacts, escalation paths, and communication templates
- **maintenance_automation.py**: Automates system maintenance tasks including scheduling, backup plans, stakeholder notifications, and health validation

## References

### Reference Documentation (`references/` directory)
- **troubleshooting.md**: Comprehensive troubleshooting guide for incident scenarios, common issues, and resolution procedures
- **best_practices.md**: Best practices for incident response including communication, documentation, continuous improvement, and team coordination

## Examples

### Example 1: Data Breach Incident Response

**Scenario:** Detected unauthorized access to customer database containing PII.

**Response Timeline:**
- **Minute 0**: Alert from security monitoring system
- **Minute 5**: Initial assessment, incident declared SEV-1
- **Minute 15**: Containment team isolated affected systems
- **Hour 1**: Forensic evidence preserved, law enforcement notified
- **Hour 4**: Affected users notified, remediation in progress
- **Week 1**: Full postmortem, regulatory reporting completed

**Key Actions:**
1. Isolate affected systems while preserving evidence
2. Identify scope of breach (records accessed)
3. Preserve logs and forensic data
4. Notify legal and compliance teams
5. Communicate with affected customers
6. Implement additional security controls

### Example 2: DDoS Attack Mitigation

**Scenario:** Distributed denial of service attack targeting API endpoints.

**Mitigation Steps:**
1. **Detection**: Automated alerts from CDN/WAF monitoring
2. **Analysis**: Identify attack vectors (HTTP flood, UDP flood)
3. **Filtering**: Apply rate limiting and IP blocklists
4. **Scaling**: Autoscaling to absorb attack traffic
5. **Communication**: Status page updates for customers

**Technical Response:**
- Enable WAF rules for attack pattern blocking
- Activate CDN DDoS protection
- Implement CAPTCHA for affected endpoints
- Scale infrastructure horizontally
- Geo-blocking for attack source regions

### Example 3: Service Outage Recovery

**Scenario:** Critical payment processing service experiencing cascading failures.

**Recovery Process:**
1. **Incident Command**: IC assigned, war room established
2. **Impact Assessment**: 30% of transactions failing
3. **Triage**: Identified database connection pool exhaustion
4. **Immediate Fix**: Restarted service with increased pool size
5. **Verification**: Monitored recovery metrics
6. **Communication**: Customer notifications during outage

**Post-Incident:**
- Root cause: Connection leak in recent deployment
- Fix: Patched leak, added monitoring
- Prevention: Added connection pool monitoring alerts

## Best Practices

### Incident Response

- **Preparation**: Maintain updated playbooks and contact lists
- **Rapid Response**: Initial assessment within 5 minutes
- **Clear Communication**: Regular status updates to stakeholders
- **Evidence Preservation**: Maintain chain of custody
- **Thorough Documentation**: Log all actions and decisions

### Team Coordination

- **Role Clarity**: IC, communications, technical lead roles
- **Escalation Paths**: Clear procedures for escalation
- **War Room**: Dedicated space for major incidents
- **Handovers**: Detailed handoffs between shifts
- **Blameless Culture**: Focus on system improvement

### Technical Response

- **Containment First**: Isolate before investigating
- **Gradual Recovery**: Bring systems back incrementally
- **Monitoring**: Watch for cascading effects
- **Verification**: Confirm full recovery before closing
- **Documentation**: Capture forensic data before cleanup

### Communication

- **Stakeholder Updates**: Regular intervals, clear language
- **Internal Channels**: Dedicated incident Slack channels
- **Customer Communication**: Transparent, empathetic messaging
- **Executive Briefings**: High-level status and impact
- **Post-Incident**: Share learnings broadly

### Continuous Improvement

- **Postmortem Culture**: Blameless, focused on improvement
- **Action Items**: Track to completion
- **Testing**: Regular incident response exercises
- **Tooling**: Automate detection and response where possible
- **Knowledge Base**: Document patterns and solutions

## Anti-Patterns

### Response Anti-Patterns

- **Panic Response**: Acting without assessment in all situations - follow triage procedures, escalate appropriately
- **Over-Containment**: Shutting down more than necessary during containment - minimize business impact
- **Premature Closure**: Declaring incident resolved before full validation - verify complete recovery
- **Documentation Debt**: Failing to document during incident - maintain real-time incident log

### Communication Anti-Patterns

- **Information Hoarding**: Limiting information to select groups - share appropriately with all stakeholders
- **Vague Updates**: Providing unclear status updates - use clear, specific language with actionable information
- **Oversharing**: Sharing sensitive details inappropriately - maintain information classification
- **Silence**: Not communicating during ongoing incidents - provide regular updates even when no new information

### Investigation Anti-Patterns

- **Tunnel Vision**: Focusing only on obvious attack vectors - consider all possibilities
- **Assumption-Based Investigation**: Assuming attack methodology without evidence - let evidence guide investigation
- **Evidence Destruction**: Cleaning systems before evidence collection - preserve evidence first
- **Scope Creep**: Expanding investigation beyond incident scope - maintain focus on incident boundaries

### Recovery Anti-Patterns

- **Rush to Restore**: Restoring service before understanding root cause - fix cause before restore
- **Partial Recovery**: Declaring recovery complete when partial - verify complete functionality
- **Configuration Drift**: Restoring to previous broken state - restore to known good baseline
- **Monitoring Neglect**: Not monitoring post-recovery - maintain heightened vigilance after incidents
