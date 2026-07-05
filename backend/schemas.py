from pydantic import BaseModel, Field
from typing import List

class CodeSubmission(BaseModel):
    filename: str
    content: str

# =====================================================================
# 1. SECURITY REPORT SCHEMA DATA STRUCTURES
# =====================================================================
class VulnerabilityItem(BaseModel):
    title: str = Field(..., description="The clear technical title of the security risk (e.g., SQL Injection).")
    category: str = Field(..., description="OWASP Top 10 classification tier identifier code.")
    severity: str = Field(..., description="Risk assessment matrix level. Must be exactly 'High', 'Medium', or 'Low'.")
    location: str = Field(..., description="The localized context inside the target code module where the risk exists.")
    line_number: int = Field(default=0, description="The integer line number identifying where the vulnerability statement is located.")
    description: str = Field(..., description="A detailed architectural breakdown of how an exploit payload could run here.")
    remediation: str = Field(..., description="The required engineering fix pattern needed to secure the exposure.")

class SecurityReport(BaseModel):
    vulnerabilities: List[VulnerabilityItem] = Field(default_factory=list, description="Array collection of security threat items.")


# =====================================================================
# 2. QA & PERFORMANCE REPORT SCHEMA DATA STRUCTURES
# =====================================================================
class QABugItem(BaseModel):
    bug_type: str = Field(..., description="The precise compiler or language runtime error flag code (e.g., NullPointerException).")
    line_number: int = Field(..., description="The exact integer line index indicating where the bug statement originates.")
    impact: str = Field(..., description="Classification category: 'Compilation Error', 'Runtime Error', 'Performance Bottleneck', or 'Informational'.")
    description: str = Field(..., description="An analytical narrative explaining why this instruction pattern crashes or slows down execution.")
    fix_suggestion: str = Field(..., description="The exact, executable code statement correction needed to clean up the bug block.")

class QAReport(BaseModel):
    bugs: List[QABugItem] = Field(default_factory=list, description="Array collection of architectural quality bug items.")