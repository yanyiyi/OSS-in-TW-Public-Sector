from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_once(text: str, old: str, new: str) -> str:
    if old not in text:
        return text
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, body: str) -> str:
    start_idx = text.find(start)
    if start_idx == -1:
        return text
    body_start = start_idx + len(start)
    end_idx = text.find(end, body_start)
    if end_idx == -1:
        return text
    return text[:body_start] + body + text[end_idx:]


def headingize(text: str, labels: list[tuple[str, str]]) -> str:
    for level, label in labels:
        pattern = re.compile(rf"(?m)^(?!#){re.escape(label)}$")
        text = pattern.sub(f"{level} {label}", text)
    return text


def normalize_blank_lines(text: str) -> str:
    text = re.sub(r"(?m)^#\n\n(#{1,5}\s)", lambda match: "#" + match.group(1), text)
    text = re.sub(r"(?<![\n#])(#{2,6}\s(?:\d|第|Chapter|Appendix|附錄|Introduction|緒論|Origin|緣起))", r"\n\n\1", text)
    lines = [line.rstrip() for line in text.splitlines()]
    out: list[str] = []

    def kind(line: str) -> str:
        stripped = line.strip()
        if not stripped:
            return "blank"
        if re.match(r"^#{1,6}\s", stripped):
            return "heading"
        if stripped.startswith("|"):
            return "table"
        if stripped.startswith("!["):
            return "image"
        if stripped.startswith("[^"):
            return "footnote"
        if stripped.startswith("- ") or re.match(r"^\d+\.\s", stripped):
            return "list"
        if stripped.startswith(("*", "_")):
            return "caption"
        return "text"

    def add(line: str) -> None:
        if line == "" and (not out or out[-1] == ""):
            return
        out.append(line)

    for idx, line in enumerate(lines):
        if not line.strip():
            prev_kind = kind(lines[idx - 1]) if idx > 0 else "blank"
            next_kind = kind(lines[idx + 1]) if idx + 1 < len(lines) else "blank"
            if prev_kind == next_kind and prev_kind in {"table", "list"}:
                continue
        add(line)
        if idx == len(lines) - 1:
            continue
        cur = kind(line)
        nxt = kind(lines[idx + 1])
        if cur == "blank" or nxt == "blank":
            continue
        if nxt in {"heading", "image"} or (nxt == "table" and cur != "table"):
            add("")
        elif cur in {"heading", "caption", "image"} or (cur == "table" and nxt != "table"):
            add("")
        elif cur == "text" and nxt in {"text", "list"}:
            add("")
        elif cur == "list" and nxt == "text":
            add("")

    return "\n".join(out).strip() + "\n"


def normalize_zh_spacing(text: str) -> str:
    # Full-width parentheses are preferred in Traditional Chinese copy.
    def repl_paren(match: re.Match[str]) -> str:
        inner = match.group(1).strip()
        return f"（{inner}）"

    text = re.sub(r"(?<=[\u4e00-\u9fff])\s*\(([^()\n]+)\)\s*(?=[\u4e00-\u9fffA-Za-z0-9])", repl_paren, text)
    text = re.sub(r"(?<=[A-Za-z0-9])\s*\(([^()\n]+)\)\s*(?=[\u4e00-\u9fff])", repl_paren, text)
    text = re.sub(r"[ \t]+（", "（", text)
    text = re.sub(r"）[ \t]+", "）", text)

    # Taiwan thesis style: separate Latin/Roman/numeric tokens from CJK text.
    text = re.sub(r"([\u4e00-\u9fff])([A-Za-z0-9][A-Za-z0-9./+&_-]*)", r"\1 \2", text)
    text = re.sub(r"([A-Za-z0-9][A-Za-z0-9./+&_-]*)([\u4e00-\u9fff])", r"\1 \2", text)
    text = re.sub(r"([\u4e00-\u9fff])([IVXLCDM]+)(?=[\u4e00-\u9fff])", r"\1 \2", text)
    text = re.sub(r"(?<=[\u4e00-\u9fff])\s+([，。；：、！？）」』])", r"\1", text)
    text = re.sub(r"([「『（])\s+", r"\1", text)
    text = re.sub(r"\s+([）])", r"\1", text)
    text = text.replace("）|", "） |")
    text = re.sub(r"(?<=\S) {2,}", " ", text)
    return text


def final_repairs(text: str, lang: str) -> str:
    text = re.sub(r"(?m)^(#{1,6})\s+\1\s+", r"\1 ", text)
    text = text.replace("code resue", "code reuse")

    if lang == "zh":
        text = re.sub(r"(?m)^ - (\[[^\]]+\]\(#)", r"  - \1", text)
        text = text.replace(
            """1. 建立分支（Branch）2. 開發與提交（Commit）3. 推送到 GitHub（Push）4. 建立 Issue
5. 建立 PR（Pull Request）6. 程式碼檢驗（Code Review）7. 合併 PR
8. 版本標記與發布（Tag & Release）""",
            """1. 建立分支（Branch）
2. 開發與提交（Commit）
3. 推送到 GitHub（Push）
4. 建立 Issue
5. 建立 PR（Pull Request）
6. 程式碼檢驗（Code Review）
7. 合併 PR
8. 版本標記與發布（Tag & Release）""",
        )
        text = text.replace(
            "##### 確保授權合規：ISO/IEC 5230（OpenChain 授權合規）ISO/IEC 5230",
            "##### 確保授權合規：ISO/IEC 5230（OpenChain 授權合規）\n\nISO/IEC 5230",
        )
        text = text.replace(
            "（若需要）- ISO/IEC 5230 相關對象",
            "（若需要）\n- ISO/IEC 5230 相關對象",
        )
        text = text.replace(
            """| 系統維運工項 | | 說明 |
| --- | --- | --- |
| | 系統監控 | 即時追蹤與分析系統運作狀態，以確保服務及效能穩定 |
| | 日誌管理 | 收集、儲存與分析系統相關紀錄，以利問題追蹤與稽核 |
| | 容量管理 | 預測與調整資源使用量，避免系統過載或資源浪費 |
| | 資安管理 | 保護系統與資料免於未授權存取、攻擊或洩漏的管理措施 |
| | 功能維護 | 持續修正錯誤與優化系統功能，確保系統穩定及符合需求 |
| | 版本控管 | 管理系統變更的歷史紀錄，確保團隊協作與版本一致性 |
| | 文件管理 | 維護系統相關文件，確保資訊完整、可追溯與易於查閱 |""",
            """| 系統維運工項 | 說明 |
| --- | --- |
| 系統監控 | 即時追蹤與分析系統運作狀態，以確保服務及效能穩定 |
| 日誌管理 | 收集、儲存與分析系統相關紀錄，以利問題追蹤與稽核 |
| 容量管理 | 預測與調整資源使用量，避免系統過載或資源浪費 |
| 資安管理 | 保護系統與資料免於未授權存取、攻擊或洩漏的管理措施 |
| 功能維護 | 持續修正錯誤與優化系統功能，確保系統穩定及符合需求 |
| 版本控管 | 管理系統變更的歷史紀錄，確保團隊協作與版本一致性 |
| 文件管理 | 維護系統相關文件，確保資訊完整、可追溯與易於查閱 |""",
        )

    if lang == "en":
        text = text.replace("JSON, XML 。", "JSON, XML.")
        text = text.replace(
            """For open-source software adopted within a project, it is recommended to use the “License Compliance Assessment Checklist for Public-Sector Use of Open-Source Software (or Public Code)” as the review tool (please refer to [Appendix V](#appendix-v-license-compliance-assessment-checklist), “License Compliance Assessment Checklist for Public-Sector Use of Open-Source Software (or Public Code)” and

[Appendix V](#appendix-v-license-compliance-assessment-checklist)I, “License Compliance Assessment Checklist Sample” of this manual). The checklist primarily includes three sections: basic project information, review items and development outcomes as public code. It assists agencies in identifying risks associated with the use of open-source software and in planning appropriate risk-mitigation measures. Based on the results of completing the assessment checklist, agencies should pay particular attention to the following items in order to strengthen the quality of risk management when using open-source software.""",
            """For open-source software adopted within a project, it is recommended to use the “License Compliance Assessment Checklist for Public-Sector Use of Open-Source Software (or Public Code)” as the review tool (see [Appendix V](#appendix-v-license-compliance-assessment-checklist)). The checklist primarily includes three sections: basic project information, review items, and development outcomes as public code. It assists agencies in identifying risks associated with the use of open-source software and in planning appropriate risk-mitigation measures. Based on the results of the checklist, agencies should pay particular attention to the following items to strengthen risk management when using open-source software.""",
        )
        text = text.replace(
            """| | Education and training | Ensure that all parties involved are equipped with the knowledge and skills essential to the fulfillment of their responsibilities and that they understand the policy clearly |
| Key | Sub-item | Description |
| --- | --- | --- |
| Management and Support |""",
            """| | Education and training | Ensure that all parties involved are equipped with the knowledge and skills essential to the fulfillment of their responsibilities and that they understand the policy clearly |
| Management and Support |""",
        )
        text = text.replace(
            """When a system integrates open-source software released under different license terms.

If a system includes code licensed under different licenses, attention must be paid to the requirements of each license. For example, when integrating GPL-licensed code with MIT- or Apache-licensed code, the resulting derivative work must comply with the GPL requirement that it “must also be licensed under the GPL”.

When there is a need to integrate code into proprietary software.

Since the GPL is a license that mandates source-code disclosure, integrating GPL-licensed code into a closed-source system that provides external services without releasing the source code would constitute a license violation.

Planning for open-source release and maintenance after go-live.

If a system is released as Public Code, appropriate resources may need to be planned to handle issues, continuously monitor community activity and establish version upgrade mechanisms and strategies (see Chapter 4 for details).""",
            """- License integration: When a system includes code licensed under different open-source licenses, attention must be paid to the requirements of each license. For example, when integrating GPL-licensed code with MIT- or Apache-licensed code, the resulting derivative work must comply with the GPL requirement that it “must also be licensed under the GPL”.
- Integration with proprietary software: Since the GPL mandates source-code disclosure, integrating GPL-licensed code into a closed-source system that provides external services without releasing the source code may constitute a license violation.
- Open-source release and maintenance after go-live: If a system is released as Public Code, appropriate resources should be planned to handle issues, continuously monitor community activity and establish version upgrade mechanisms and strategies (see Chapter 4 for details).""",
        )
        text = text.replace(
            """| Description of O&M Work Items | |
| --- | --- |
| System Monitoring | Real-time tracking and analysis of system operation to ensure service and performance stability. |
| Log Management | Collect, store and analyze system logs for troubleshooting and audits. |
| Capacity Management | Forecast and adjust resource usage to prevent overloads or resource waste. |
| Information Security Management | Measures to protect systems and data from unauthorized access, attacks or leakage. |
| Functional Maintenance | Continuous bug fixes and system optimization to ensure stability and alignment with requirements. |
| Version Control | Management of change log to support collaboration and maintain version consistency. |
| Documentation Management | Maintenance of system documentation to ensure completeness, traceability and ease of reference. |""",
            """| O&M Work Item | Description |
| --- | --- |
| System Monitoring | Real-time tracking and analysis of system operation to ensure service and performance stability. |
| Log Management | Collect, store and analyze system logs for troubleshooting and audits. |
| Capacity Management | Forecast and adjust resource usage to prevent overloads or resource waste. |
| Information Security Management | Measures to protect systems and data from unauthorized access, attacks or leakage. |
| Functional Maintenance | Continuous bug fixes and system optimization to ensure stability and alignment with requirements. |
| Version Control | Management of change log to support collaboration and maintain version consistency. |
| Documentation Management | Maintenance of system documentation to ensure completeness, traceability and ease of reference. |""",
        )
        text = text.replace(
            """##### Open-Source Software Sustainability Strategy

Open-source talent development and culture building.

Community activity monitoring and continuous integration.

Establishment of system management and upgrade strategies.

License management and code reuse.

Connecting communities and public code platforms.""",
            """##### Open-Source Software Sustainability Strategy

- Open-source talent development and culture building.
- Community activity monitoring and continuous integration.
- Establishing system management and upgrade strategies.
- License management and code reuse.
- Connecting communities and public code platforms.""",
        )
        text = text.replace(
            """| 3 | Are other developed countries’ governments also promoting Public Code? | 。Many countries are actively promoting Public Code policies, treating government-developed information and communication systems’ source code as public assets and making them open for public use. For example, Estonia, Finland |
| | | and Iceland jointly maintain the open-source X-Road system, allowing governments to freely use it domestically and submit fixes when issues are discovered so that other entities can update simultaneously. The United Kingdom has also modularized internal government form-design and submission mechanisms into independent services that can be shared not only across UK government agencies but also applied for by other countries’ governments. |""",
            """| 3 | Are other developed countries’ governments also promoting Public Code? | Many countries are actively promoting Public Code policies, treating government-developed information and communication systems’ source code as public assets and making them open for public use. For example, Estonia, Finland and Iceland jointly maintain the open-source X-Road system, allowing governments to freely use it domestically and submit fixes when issues are discovered so that other entities can update simultaneously. The United Kingdom has also modularized internal government form-design and submission mechanisms into independent services that can be shared not only across UK government agencies but also applied for by other countries’ governments. |""",
        )
        text = text.replace("| | □ Risk Analysis and Security Design | .To ensure", "| | □ Risk Analysis and Security Design | To ensure")
        text = text.replace("□Yes", "□ Yes")

    text = remove_repeated_table_headers(text)
    return text


def remove_repeated_table_headers(text: str) -> str:
    lines = text.splitlines()
    out: list[str] = []
    i = 0

    def is_table(line: str) -> bool:
        return line.startswith("|")

    def is_separator(line: str) -> bool:
        return bool(re.match(r"^\|\s*:?-{3,}:?\s*(?:\|\s*:?-{3,}:?\s*)+\|?$", line))

    while i < len(lines):
        if (
            i + 1 < len(lines)
            and is_table(lines[i])
            and is_separator(lines[i + 1])
            and out
            and is_table(out[-1])
            and not is_separator(out[-1])
        ):
            i += 2
            continue
        out.append(lines[i])
        i += 1

    return "\n".join(out).strip() + "\n"


def fix_zh() -> None:
    path = ROOT / "ZH_TW.md"
    text = path.read_text(encoding="utf-8")

    text = headingize(
        text,
        [
            ("#####", "實踐開源軟體政策的標竿案例"),
            ("#####", "管理軟體物料清單（SBOM 表）"),
            ("#####", "SBOM 表核心功能說明"),
            ("#####", "主要 SBOM 格式比較：SPDX vs. CycloneDX"),
            ("#####", "全球公部門 OSPO 的崛起"),
            ("#####", "確保授權合規：ISO/IEC 5230（OpenChain 授權合規）"),
            ("#####", "ISO/IEC 5230 關鍵實踐重點"),
            ("#####", "OpenChain 安全保障：ISO/IEC 18974"),
            ("#####", "ISO/IEC 18974 關鍵實踐重點"),
            ("#####", "常見之共通性功能模組"),
            ("#####", "自動化治理重點"),
            ("#####", "可讀且完整的技術文件"),
            ("#####", "可合法修改再利用的授權模式"),
            ("#####", "最終交付文件包整備"),
            ("#####", "視需求決定不同的公共程式維護等級"),
            ("#####", "核心治理文件"),
            ("#####", "日誌管理四大重點"),
            ("#####", "開源軟體 Issue 追蹤處理流程"),
            ("#####", "GitHub 版本控管流程示例"),
            ("#####", "開源軟體永續經營五大策略"),
        ],
    )
    text = re.sub(r"(?m)^3\. 認證路徑$", "##### 認證路徑", text)

    text = text.replace("##### Case Study 1 ： 我國企業導入開源政策典範- KKCompany", "##### Case Study 1：我國企業導入開源政策典範 - KKCompany")
    text = text.replace("##### Case Study 2 ： 美國聯邦政府國土安全部", "##### Case Study 2：美國聯邦政府國土安全部")
    text = text.replace("##### Case Study 3 ： 美國聯邦政府醫療保險和醫療補助服務中心", "##### Case Study 3：美國聯邦政府醫療保險和醫療補助服務中心")
    text = text.replace("##### Case Study 4 ： 臺北市政府資訊局", "##### Case Study 4：臺北市政府資訊局")
    text = re.sub(r"(?m)^(##### 管理軟體物料清單（SBOM 表）)(在所有)", r"\1\n\n\2", text)

    text = replace_once(
        text,
        """| 社群參與 | 貢獻政策 | 制定明確的政策，規範組織員工對外部開源專案的貢獻行為。 |
ISO/IEC 5230 關鍵產物：
完整的授權聲明、姓名標示文件、原始碼提供（若需要）
ISO/IEC 5230 相關對象：
法務部門、採購部門、軟體開發團隊、OSPO""",
        """| 社群參與 | 貢獻政策 | 制定明確的政策，規範組織員工對外部開源專案的貢獻行為。 |

- ISO/IEC 5230 關鍵產物：完整的授權聲明、姓名標示文件、原始碼提供（若需要）
- ISO/IEC 5230 相關對象：法務部門、採購部門、軟體開發團隊、OSPO""",
    )
    text = replace_once(
        text,
        """| | 客戶溝通 | 在必要時，有方法將已識別的漏洞資訊傳達給受影響的用戶或客戶。 |
ISO/IEC 18974 關鍵產物：
漏洞清單、風險評估報告、修補計畫與紀錄
ISO/IEC 18974 相關對象：
資安部門、維運團隊（DevSecOps）、軟體開發團隊、OSPO
ISO/IEC 5230 與 ISO/IEC 18974 兩者相輔相成。""",
        """| | 客戶溝通 | 在必要時，有方法將已識別的漏洞資訊傳達給受影響的用戶或客戶。 |

- ISO/IEC 18974 關鍵產物：漏洞清單、風險評估報告、修補計畫與紀錄
- ISO/IEC 18974 相關對象：資安部門、維運團隊（DevSecOps）、軟體開發團隊、OSPO

ISO/IEC 5230 與 ISO/IEC 18974 兩者相輔相成。""",
    )
    text = replace_once(
        text,
        """上述標準的合規認證可以透過以下兩種途徑取得：

自我認證
第三方認證
機關可聘請經認可的獨立驗證機構進行稽核。通過稽核後，將獲得正式的符合性證書。
此方式如同 KKCompany 的案例所示，能為組織的開源治理能力提供強而有力的外部背書，對於建立客戶、合作夥伴及監管機構的信任至關重要。
OpenChain 計畫免費提供線上查檢表。
機關可利用此工具進行內部稽核與差距分析，逐一檢視是否滿足所有要求。""",
        """上述標準的合規認證可以透過以下兩種途徑取得：

- 自我認證：OpenChain 計畫免費提供線上查檢表，機關可利用此工具進行內部稽核與差距分析，逐一檢視是否滿足所有要求。
- 第三方認證：機關可聘請經認可的獨立驗證機構進行稽核。通過稽核後，將獲得正式的符合性證書。此方式如同 KKCompany 的案例所示，能為組織的開源治理能力提供強而有力的外部背書，對於建立客戶、合作夥伴及監管機構的信任至關重要。""",
    )

    text = replace_once(
        text,
        """開源軟體評估與選型流程主要分為五個步驟，以下將逐一說明。針對規劃之完整性，可參考 [附錄四](#appendix-iv-requirements-planning-self-assessment-checklist)「公部門專案導入開源軟體（或公共程式）需求規劃自主檢核表」進行自主檢核。
1. 需求釐清，識別專案目標與限制
確認本次專案的核心目標，並規劃系統所需具備的功能，以設定規格要求，確保能支援預期的使用對象及情境。於此同時，應檢視是否存在法規或資安政策的限制，例如個資保護要求、機關內部的安全規範的適用性，避免後續導入時衍生相關風險，以確定系統選型的基本條件。
2. 模組化需求，以可擴充參與的規格取代過度設計""",
        """開源軟體評估與選型流程主要分為五個步驟，以下將逐一說明。針對規劃之完整性，可參考 [附錄四](#appendix-iv-requirements-planning-self-assessment-checklist)「公部門專案導入開源軟體（或公共程式）需求規劃自主檢核表」進行自主檢核。

##### 1. 需求釐清，識別專案目標與限制

確認本次專案的核心目標，並規劃系統所需具備的功能，以設定規格要求，確保能支援預期的使用對象及情境。於此同時，應檢視是否存在法規或資安政策的限制，例如個資保護要求、機關內部的安全規範的適用性，避免後續導入時衍生相關風險，以確定系統選型的基本條件。

##### 2. 模組化需求，以可擴充參與的規格取代過度設計""",
    )
    text = re.sub(r"(?m)^3\. 潛在開源軟體盤點，搜尋合適的開源專案$", "##### 3. 潛在開源軟體盤點，搜尋合適的開源專案", text)
    text = re.sub(r"(?m)^4\. 元件選用評估：三大檢核點$", "##### 4. 元件選用評估：三大檢核點", text)
    text = re.sub(r"(?m)^5\. 風險分析：防患於未然$", "##### 5. 風險分析：防患於未然", text)
    text = replace_once(
        text,
        """為此，每一個被納入政府專案的開源元件，都建議依循開源政策，通過以下三大檢核點。
授權相容性
深入分析元件的授權條款，特別注意 GPL 這類具備「感染性」的授權，是否會與專案中其他專有授權的元件產生衝突。
安全狀況
檢視該元件是否存在已知的安全漏洞（CVEs），以及其維護團隊是否有長期、穩定的安全更新紀錄。
社群健康度
一個健康的社群是專案能否長久維護的關鍵。應評估該專案是否有活躍的維護者、貢獻者，以及社群的討論氛圍是否友善開放。""",
        """為此，每一個被納入政府專案的開源元件，都建議依循開源政策，通過以下三大檢核點。

- 授權相容性：深入分析元件的授權條款，特別注意 GPL 這類具備「感染性」的授權，是否會與專案中其他專有授權的元件產生衝突。
- 安全狀況：檢視該元件是否存在已知的安全漏洞（CVEs），以及其維護團隊是否有長期、穩定的安全更新紀錄。
- 社群健康度：一個健康的社群是專案能否長久維護的關鍵。應評估該專案是否有活躍的維護者、貢獻者，以及社群的討論氛圍是否友善開放。""",
    )
    text = replace_once(
        text,
        """威脅建模：在設計階段就應預測系統可能面臨的攻擊面，並規劃對應的防禦機制。
資料設計：特別是涉及個人可識別資訊的架構，必須事先進行嚴謹的規劃與加密設計，避免日後因架構問題而難以修補。""",
        """- 威脅建模：在設計階段就應預測系統可能面臨的攻擊面，並規劃對應的防禦機制。
- 資料設計：特別是涉及個人可識別資訊的架構，必須事先進行嚴謹的規劃與加密設計，避免日後因架構問題而難以修補。""",
    )

    text = replace_once(
        text,
        """SBOM 與 CI/CD 整合
版本控制
以 Git 作為版本控制的基礎，並採用清晰的分支策略與提交訊息規範，讓每一次的版本差異都明確可追溯。
在持續整合／持續部署的自動化流程中，加入自動生成與檢查軟體物料清單 SBOM 的步驟，確保每一次建構（Build）的產出，所有依賴元件都是清晰可查的。
自動化合規檢核
漏洞修補與紀錄
建立標準化的漏洞修補流程，並詳實追蹤修補的歷史紀錄，確保軟體基底的成熟度與安全性是透明且可被驗證的。
在測試環節中，應同步整合自動化工具，進行授權掃描、合規檢查與漏洞掃描。""",
        """版本控制與自動化整合的重點可整理如下：

- 版本控制：以 Git 作為版本控制的基礎，並採用清晰的分支策略與提交訊息規範，讓每一次的版本差異都明確可追溯。
- SBOM 與 CI/CD 整合：在持續整合／持續部署的自動化流程中，加入自動生成與檢查軟體物料清單 SBOM 的步驟，確保每一次建構（Build）的產出，所有依賴元件都是清晰可查的。
- 自動化合規檢核：在測試環節中，應同步整合自動化工具，進行授權掃描、合規檢查與漏洞掃描。
- 漏洞修補與紀錄：建立標準化的漏洞修補流程，並詳實追蹤修補的歷史紀錄，確保軟體基底的成熟度與安全性是透明且可被驗證的。""",
    )
    text = replace_once(
        text,
        """版本控制
以 Git 作為版本控制基礎。
清晰分支策略與提交訊息規範。

SBOM 與 CI/CD 整合
加入自動生成與檢查軟體物料清單的步驟。

自動化合規檢核
應包含授權掃描、合規檢查和漏洞掃描。

漏洞修補與紀錄
建立標準化漏洞修補流程。
詳實追蹤修補歷史紀錄。""",
        """| 重點 | 說明 |
| --- | --- |
| 版本控制 | 以 Git 作為版本控制基礎，搭配清晰分支策略與提交訊息規範。 |
| SBOM 與 CI/CD 整合 | 加入自動生成與檢查軟體物料清單的步驟。 |
| 自動化合規檢核 | 應包含授權掃描、合規檢查和漏洞掃描。 |
| 漏洞修補與紀錄 | 建立標準化漏洞修補流程，並詳實追蹤修補歷史紀錄。 |""",
    )

    text = replace_once(
        text,
        """安裝編譯軟體
從零開始建立開發環境
安裝所有必要的相依套件
理解整體的架構
將軟體部署至生產環境""",
        """- 安裝編譯軟體
- 從零開始建立開發環境
- 安裝所有必要的相依套件
- 理解整體的架構
- 將軟體部署至生產環境""",
    )
    text = replace_once(text, "再製權\n轉授權", "- 再製權\n- 轉授權")
    text = replace_once(text, "資安風險評估報告\n授權檢核報告\n軟體物料清單（SBOM）", "- 資安風險評估報告\n- 授權檢核報告\n- 軟體物料清單（SBOM）")

    text = replace_once(
        text,
        """等級 0 - 1（Tier 0-1）：僅原始碼存檔
適用情境：已完成其階段性任務、不再進行活躍開發的專案。例如，為某個一次性大型活動所開發的網站、已結案的研究計畫所使用的分析工具等，未來大幅度的更新機率不高，亦可考量其為等級 0 ，或者未來持續可能偶一為之時選擇等級 1 。
治理重點：明確地在專案的 README 文件和網站上標示該專案已「封存」（Archived）。原始碼和文件將繼續公開存放，以供歷史查閱、學術研究或他人參考，但官方不再提供任何形式的支援、頻繁更新或安全保證，但其依然為具有價值得以讓其他單位參考運用的專案。
等級 2（Tier 2）：官方長期維護
適用情境：支撐核心公共服務、具備高度戰略意義的關鍵系統。例如，報稅系統、數位身分驗證服務、災防告警系統等。
治理重點：由政府編列常態性預算，組建專職的內部團隊或委託專業廠商進行持續的開發、維護與安全更新。這是最高等級的承諾，確保系統的穩定與可靠。
等級 3-4（Tier 3-4）：轉交社群託管
適用情境：具有高度實用價值、已形成活躍使用者或貢獻者社群，但非屬關鍵基礎設施的工具或平臺。例如，資料視覺化工具、內部專案管理範本、政府網站設計系統等。
治理重點：政府的角色從「主導開發者」轉變為「社群賦能者」。政府不再負責所有程式碼的撰寫，而是提供必要的基礎設施（如程式碼託管、論壇）、建立清晰的治理規則，並鼓勵、引導社群成員接手主要的維護與發展工作。""",
        """| 維護等級 | 適用情境 | 治理重點 |
| --- | --- | --- |
| 等級 0 - 1（Tier 0-1）：僅原始碼存檔 | 已完成其階段性任務、不再進行活躍開發的專案。例如，為某個一次性大型活動所開發的網站、已結案的研究計畫所使用的分析工具等，未來大幅度的更新機率不高，亦可考量其為等級 0，或者未來持續可能偶一為之時選擇等級 1。 | 明確地在專案的 README 文件和網站上標示該專案已「封存」（Archived）。原始碼和文件將繼續公開存放，以供歷史查閱、學術研究或他人參考，但官方不再提供任何形式的支援、頻繁更新或安全保證，但其依然為具有價值得以讓其他單位參考運用的專案。 |
| 等級 2（Tier 2）：官方長期維護 | 支撐核心公共服務、具備高度戰略意義的關鍵系統。例如，報稅系統、數位身分驗證服務、災防告警系統等。 | 由政府編列常態性預算，組建專職的內部團隊或委託專業廠商進行持續的開發、維護與安全更新。這是最高等級的承諾，確保系統的穩定與可靠。 |
| 等級 3-4（Tier 3-4）：轉交社群託管 | 具有高度實用價值、已形成活躍使用者或貢獻者社群，但非屬關鍵基礎設施的工具或平臺。例如，資料視覺化工具、內部專案管理範本、政府網站設計系統等。 | 政府的角色從「主導開發者」轉變為「社群賦能者」。政府不再負責所有程式碼的撰寫，而是提供必要的基礎設施（如程式碼託管、論壇）、建立清晰的治理規則，並鼓勵、引導社群成員接手主要的維護與發展工作。 |""",
    )

    text = replace_once(
        text,
        """CONTRIBUTING.md
詳細說明如何提交程式碼貢獻（例如，如何開設 issue、發起 pull request、編碼風格要求、需要包含測試等）

CODE_OF_CONDUCT.md
明確訂定社群的行為準則，確保這是一個尊重、包容與專業的協作環境

治理模型文件（GOVERNANCE.md）
說明專案的決策流程、主要維護者的角色與職責等

議題追蹤
所有錯誤回報、功能建議與技術討論，都應在公開的議題追蹤系統上進行。

程式碼審查
所有來程式碼貢獻，都必須經過至少一位維護者的審查，確認其架構、風格與安全標準，才能被合併到主分支中""",
        """| 要素 | 說明 |
| --- | --- |
| CONTRIBUTING.md | 詳細說明如何提交程式碼貢獻（例如，如何開設 issue、發起 pull request、編碼風格要求、需要包含測試等）。 |
| CODE_OF_CONDUCT.md | 明確訂定社群的行為準則，確保這是一個尊重、包容與專業的協作環境。 |
| 治理模型文件（GOVERNANCE.md） | 說明專案的決策流程、主要維護者的角色與職責等。 |
| 議題追蹤 | 所有錯誤回報、功能建議與技術討論，都應在公開的議題追蹤系統上進行。 |
| 程式碼審查 | 所有來程式碼貢獻，都必須經過至少一位維護者的審查，確認其架構、風格與安全標準，才能被合併到主分支中。 |""",
    )

    text = replace_once(
        text,
        """日誌管理四大重點
結構化日誌
集中化收集
將分散於不同伺服器與服務的日誌集中在同一平臺，便於查詢與分析
使用 JSON 或統一格式，讓系統能自動化解析與比對
合規與稽核
即時搜尋與分析
快速查找特定錯誤或模式，例如異常流量來源
保存必要的日誌紀錄，滿足安全與法律規範（如 GDPR、ISO 27001）""",
        """##### 日誌管理四大重點

| 重點 | 說明 |
| --- | --- |
| 結構化日誌 | 使用 JSON 或統一格式，讓系統能自動化解析與比對。 |
| 集中化收集 | 將分散於不同伺服器與服務的日誌集中在同一平臺，便於查詢與分析。 |
| 合規與稽核 | 保存必要的日誌紀錄，滿足安全與法律規範（如 GDPR、ISO 27001）。 |
| 即時搜尋與分析 | 快速查找特定錯誤或模式，例如異常流量來源。 |""",
    )
    text = replace_once(
        text,
        """開源軟體 Issue 追蹤處理流程
討論與補充資訊
分類與標籤
建立 Issue
版本發布與紀錄
PR 審查與合併
修復與提交 PR
使用者/開發者在專案的 issue tracker 中提交問題，內容應包含標題、描述、重現步驟、預期結果與實際結果等資訊
專案維護者會根據問題性質加上標籤（如 bug、question、security），並指派給相關開發者或團隊
開發者與社群成員可在 issue 下方留言，釐清問題、提供重現方式或提出解法建議
開發者根據 issue 修正程式碼，並提交 PR（Pull Request），通常會在 PR 中關聯對應的 issue（例如 Fixes #123）
維護者審查 PR，確認修正無誤後合併至主分支，並關閉對應的 issue
修正內容會在下個版本中釋出，並記錄於 changelog 中，供使用者參考""",
        """##### 開源軟體 Issue 追蹤處理流程

| 流程 | 說明 |
| --- | --- |
| 建立 Issue | 使用者/開發者在專案的 issue tracker 中提交問題，內容應包含標題、描述、重現步驟、預期結果與實際結果等資訊。 |
| 分類與標籤 | 專案維護者會根據問題性質加上標籤（如 bug、question、security），並指派給相關開發者或團隊。 |
| 討論與補充資訊 | 開發者與社群成員可在 issue 下方留言，釐清問題、提供重現方式或提出解法建議。 |
| 修復與提交 PR | 開發者根據 issue 修正程式碼，並提交 PR（Pull Request），通常會在 PR 中關聯對應的 issue（例如 Fixes #123）。 |
| PR 審查與合併 | 維護者審查 PR，確認修正無誤後合併至主分支，並關閉對應的 issue。 |
| 版本發布與紀錄 | 修正內容會在下個版本中釋出，並記錄於 changelog 中，供使用者參考。 |""",
    )
    text = replace_once(
        text,
        """建立分支
（Branch）
開發與提交
（Commit）
推送到 GitHub
（Push）
建立 Issue

建立 PR
（Pull Request）
程式碼檢驗
（Code Review）
版本標記&發布
（Tag & Release）
合併 PR""",
        """1. 建立分支（Branch）
2. 開發與提交（Commit）
3. 推送到 GitHub（Push）
4. 建立 Issue
5. 建立 PR（Pull Request）
6. 程式碼檢驗（Code Review）
7. 合併 PR
8. 版本標記與發布（Tag & Release）""",
    )
    text = replace_once(
        text,
        """開源軟體永續經營五大策略
開源人才培育與文化形塑
社群動態追蹤與持續整合
系統管理與升級策略建立
授權條款管理與程式碼再利用
連結社群與公共程式平臺""",
        """##### 開源軟體永續經營五大策略

- 開源人才培育與文化形塑
- 社群動態追蹤與持續整合
- 系統管理與升級策略建立
- 授權條款管理與程式碼再利用
- 連結社群與公共程式平臺""",
    )

    text = final_repairs(normalize_zh_spacing(normalize_blank_lines(text)), "zh")
    path.write_text(text, encoding="utf-8")


def fix_en() -> None:
    path = ROOT / "EN.md"
    text = path.read_text(encoding="utf-8")

    text = headingize(
        text,
        [
            ("#####", "Benchmark Case Study of the Implementation of Open-Source Software Policy"),
            ("#####", "Case Study 1: KKCompany, the Model Company for Implementing Open-Source Policy in Taiwan"),
            ("#####", "Case Study 2: Department of Homeland Security, the USA"),
            ("#####", "Case Study 3: Centers for Medicare & Medicaid Services (CMS)"),
            ("#####", "Case Study 4: Department of Information Technology, Taipei City Government"),
            ("#####", "Software Bill of Materials (SBOM) Management"),
            ("#####", "Core Features of SBOM"),
            ("#####", "SPDX vs. CycloneDX Comparison"),
            ("#####", "The Global Emergence of OSPO at the Public Sector"),
            ("#####", "Ensuring License Compliance: ISO/IEC 5230 (OpenChain License Compliance)"),
            ("#####", "Keys to the Implementation of ISO/IEC 5230"),
            ("#####", "OpenChain Security Protection: ISO/IEC 18974"),
            ("#####", "ISO/IEC 18974 Key Practices"),
            ("#####", "Common & Universal Functional Modules"),
            ("#####", "Automated governance key points"),
            ("#####", "Readable and complete technical documentation"),
            ("#####", "License Models That Allow Legal Modification and Reuse"),
            ("#####", "Preparation of the Final Deliverables Package"),
            ("#####", "Determining Different Public Code Maintenance Levels Based on Needs"),
            ("#####", "Core governance documents"),
            ("#####", "Four Key Areas for Log Management"),
            ("#####", "Open-Source Software Issue Tracking and Resolution Workflow"),
            ("#####", "GitHub Version Control Process Diagram"),
            ("#####", "Open-Source Software Sustainability Strategy"),
        ],
    )
    text = re.sub(r"(?m)^3\. Certification Pathway: Build Trust$", "##### Certification Pathway", text)

    text = text.replace("*CC By 4.0 “FLOSS-PSO Community Map” Resource: OSPO Alliance\nIf agencies", "*CC By 4.0 “FLOSS-PSO Community Map” Resource: OSPO Alliance*\n\nIf agencies")
    text = text.replace("continuous deployment(CI/CD)", "continuous deployment (CI/CD)")
    text = text.replace("United Kingdom,did", "United Kingdom, did")
    text = text.replace("version.Long-term", "version. Long-term")
    text = text.replace("license management and code resue", "license management and code reuse")

    text = replace_once(
        text,
        """| Community Engagement | Contribution policy | Formulate a clear policy regulating organization employees’ contribution behavior for external open-source projects. |
ISO/IEC 5230 Key Documents:
Provide complete license agreement, attribution document and source code (if necessary)
ISO/IEC 5230 Target
The legal department, procurement department, software development team and OSPO""",
        """| Community Engagement | Contribution policy | Formulate a clear policy regulating organization employees’ contribution behavior for external open-source projects. |

- ISO/IEC 5230 key documents: Complete license notices, attribution documents, and source-code offer where required.
- ISO/IEC 5230 target roles: Legal department, procurement department, software development team, and OSPO.""",
    )
    text = replace_once(
        text,
        """| | Client communication | There must be a method to send the information related to the vulnerability to impacted users or clients if necessary. |
ISO/IEC 18974 Key documents:
Vulnerability list, risk evaluation report, patching schedule and record
ISO/IEC 18974 Target:
Information security department, DevSecOps, software development team and OSPO""",
        """| | Client communication | There must be a method to send the information related to the vulnerability to impacted users or clients if necessary. |

- ISO/IEC 18974 key documents: Vulnerability list, risk evaluation report, patching schedule, and patching records.
- ISO/IEC 18974 target roles: Information security department, DevSecOps team, software development team, and OSPO.""",
    )
    text = replace_once(
        text,
        """Certified compliance with the standards above can be obtained via the two pathways below:
Self-certification
Third-party certification
Organizations can hire an independent certification organization to audit them. Once they pass the audit, they will receive the official conformance certification.
As shown in the KKCompany’s example, this method can provides a strong external endorsement for an organization’s open-source governance capacity, which is crucial for building trust with clients, partners and even regulatory agencies.
OpenChain provides a free self-certification chart online.
Organizations can use this chart for internal audit and gap analysis and determine if they have met all requirements in the chart.""",
        """Certified compliance with the standards above can be obtained via two pathways:

- Self-certification: OpenChain provides a free online self-certification checklist. Organizations can use it for internal audits and gap analysis to determine whether they meet the requirements.
- Third-party certification: Organizations can hire an accredited independent certification body to conduct an audit. Once they pass the audit, they receive an official conformance certificate. As shown in KKCompany’s example, this method provides a strong external endorsement of an organization’s open-source governance capacity and is important for building trust with clients, partners, and regulators.""",
    )

    text = replace_once(
        text,
        """The open-source software evaluation and selection process is mainly divided into five steps, which are explained one by one below. To ensure completeness in planning, agencies may refer to [Appendix IV](#appendix-iv-requirements-planning-self-assessment-checklist), “Self-Assessment Checklist for Public-Sector Project Adoption of Open-Source Software (or Public Code) Requirements Planning,” to conduct a self-review.
1. Clarify requirements and identify project objectives and constraints
Confirm the core objectives of the project and plan the functions that the system requires in order to define specification requirements, ensuring support for the intended users and usage scenarios. At the same time, review whether there are regulatory or information-security policy constraints, such as personal data protection requirements or the applicability of internal organizational security standards to avoid risks arising during later adoption and to establish the basic conditions for selecting the type of software.
2. Modularize requirements, replacing overdesign with extensible and participatory specifications""",
        """The open-source software evaluation and selection process is mainly divided into five steps, which are explained one by one below. To ensure completeness in planning, agencies may refer to [Appendix IV](#appendix-iv-requirements-planning-self-assessment-checklist), “Self-Assessment Checklist for Public-Sector Project Adoption of Open-Source Software (or Public Code) Requirements Planning,” to conduct a self-review.

##### 1. Clarify requirements and identify project objectives and constraints

Confirm the core objectives of the project and plan the functions that the system requires in order to define specification requirements, ensuring support for the intended users and usage scenarios. At the same time, review whether there are regulatory or information-security policy constraints, such as personal data protection requirements or the applicability of internal organizational security standards to avoid risks arising during later adoption and to establish the basic conditions for selecting the type of software.

##### 2. Modularize requirements, replacing overdesign with extensible and participatory specifications""",
    )
    text = re.sub(r"(?m)^3\. Inventory potential open-source software and search for suitable projects$", "##### 3. Inventory potential open-source software and search for suitable projects", text)
    text = re.sub(r"(?m)^4\. Component selection evaluation: 3 key checkpoints$", "##### 4. Component selection evaluation: three key checkpoints", text)
    text = re.sub(r"(?m)^5\. Risk analysis: Prevention is Better Than Cure$", "##### 5. Risk analysis: prevention is better than cure", text)
    text = replace_once(
        text,
        """incorporated into government projects follow open-source policy and pass the following three key checkpoints.
Conduct an in-depth analysis of the component’s license terms, paying particular attention to “copyleft” licenses such as the GPL and whether they may conflict with other proprietary-licensed components in the project.
License compatibility
Security
Review whether the component has any known security vulnerabilities (CVEs) and whether its maintenance team has a long-term and stable record of issuing security updates.
A healthy community is key to whether a project can be maintained over the long term. Assess whether the project has active maintainers and contributors and whether the community’s discussion environment is friendly and open.
Community health""",
        """incorporated into government projects follow open-source policy and pass the following three key checkpoints.

- License compatibility: Conduct an in-depth analysis of the component’s license terms, paying particular attention to “copyleft” licenses such as the GPL and whether they may conflict with other proprietary-licensed components in the project.
- Security: Review whether the component has any known security vulnerabilities (CVEs) and whether its maintenance team has a long-term and stable record of issuing security updates.
- Community health: A healthy community is key to whether a project can be maintained over the long term. Assess whether the project has active maintainers and contributors and whether the community’s discussion environment is friendly and open.""",
    )
    text = replace_once(
        text,
        """Threat modeling: Potential attacks should be anticipated during the design phase with corresponding defense mechanisms planned in advance.
Data design: Especially for architectures involving personally identifiable information, rigorous planning and encryption design must be carried out upfront to avoid architectural flaws that are difficult to remediate later.""",
        """- Threat modeling: Potential attacks should be anticipated during the design phase with corresponding defense mechanisms planned in advance.
- Data design: Especially for architectures involving personally identifiable information, rigorous planning and encryption design must be carried out upfront to avoid architectural flaws that are difficult to remediate later.""",
    )

    text = replace_once(
        text,
        """Integration of SBOM and CI/CD
Version control
Use Git as the foundation for version control and adopt clear forking strategies and commit-message conventions so that every version difference is clearly traceable.
In continuous integration/continuous deployment (CI/CD) automated pipelines, include steps to automatically generate and inspect Software Bill of Materials (SBOMs), ensuring that for every build, all dependency components are clearly identifiable.
Automated compliance checks
Vulnerability patching and record
Establish standardized vulnerability patching processes and thoroughly track patching histories, ensuring that the maturity and security of the software foundation are transparent and verifiable.
During the testing phase, automated tools should be integrated concurrently to perform license scanning, compliance checks and vulnerability scanning.""",
        """The key points of version control and automated integration can be organized as follows:

- Version control: Use Git as the foundation for version control and adopt clear branching strategies and commit-message conventions so that every version difference is clearly traceable.
- SBOM and CI/CD integration: In continuous integration/continuous deployment (CI/CD) automated pipelines, include steps to automatically generate and inspect Software Bill of Materials (SBOMs), ensuring that for every build, all dependency components are clearly identifiable.
- Automated compliance checks: During the testing phase, automated tools should be integrated concurrently to perform license scanning, compliance checks, and vulnerability scanning.
- Vulnerability patching and records: Establish standardized vulnerability patching processes and thoroughly track patching histories, ensuring that the maturity and security of the software foundation are transparent and verifiable.""",
    )
    text = replace_once(
        text,
        """Version control
Use Git as the foundation for version control and adopt clear forking strategies and commit-message conventions.

Integration of SBOM and CI/CD
Include steps to automatically generate and inspect Software Bill of Materials (SBOMs).

Automated compliance checks
Perform license scanning, compliance checks and vulnerability scanning.

Vulnerability patching and record
Establish standardized vulnerability patching processes and thoroughly track patching histories.""",
        """| Key Point | Description |
| --- | --- |
| Version control | Use Git as the foundation for version control and adopt clear branching strategies and commit-message conventions. |
| SBOM and CI/CD integration | Include steps to automatically generate and inspect Software Bill of Materials (SBOMs). |
| Automated compliance checks | Perform license scanning, compliance checks, and vulnerability scanning. |
| Vulnerability patching and records | Establish standardized vulnerability patching processes and thoroughly track patching histories. |""",
    )

    text = replace_once(
        text,
        """Install all required dependency components
Establish a development environment from scratch
Install and compile the software
Deploy the software to the production environment
Understand the overall architecture""",
        """- Install all required dependency components
- Establish a development environment from scratch
- Install and compile the software
- Understand the overall architecture
- Deploy the software to the production environment""",
    )
    text = replace_once(text, "##### License Models That Allow Legal Modification and Reuse\n##### License Models That Allow Legal Modification and Reuse", "##### License Models That Allow Legal Modification and Reuse")
    text = replace_once(text, "Reproduction rights\nSublicensing rights", "- Reproduction rights\n- Sublicensing rights")
    text = replace_once(text, "Information security risk assessment report\nLicense compliance report\nSoftware Bill of Materials (SBOM)", "- Information security risk assessment report\n- License compliance report\n- Software Bill of Materials (SBOM)")

    text = replace_once(
        text,
        """Tier 0–1: Source Code Archive Only
Applicable scenarios: Projects that have completed their phase-based objectives and are no longer under active development. Examples include websites developed for one-time large-scale events or analysis tools used in completed research projects. These projects are highly unlikely to receive major future updates. Tier 0 may apply to projects with only a single contributor, while Tier 1 may apply when occasional future updates are possible.
Governance focus: Clearly mark the project as “Archived” in the “README” file and on the project website. Source code and documentation remain publicly available for reference, academic research or reuse by others, but no official support, frequent updates or security guarantees are provided. Nevertheless, such projects may still hold value for reference and reuse by other organization.
Tier 2: Official Long-Term Support
Applicable scenarios: Critical systems that support core public services and have high strategic importance, such as tax filing system, digital identity services or Public Warning System.
Governance focus: The government allocates recurring budgets and forms dedicated internal teams or commissions professional vendors to carry out continuous development, maintenance and security updates. This represents the highest level of commitment, ensuring system stability and reliability.

Tier 3–4: Community Stewardship
Applicable scenarios: Highly practical tools or platforms that have formed active user or contributor communities but are not classified as critical infrastructure, such as data visualization tools, internal project management templates or government website design systems.
Governance focus: The government’s role shifts from “lead developer” to “community enabler.” Instead of writing all code, the government provides essential infrastructure (such as code repositories and forums), establishes clear governance rules and encourages and guides community members to take on primary maintenance and development responsibilities.""",
        """| Maintenance Level | Applicable Scenarios | Governance Focus |
| --- | --- | --- |
| Tier 0–1: Source Code Archive Only | Projects that have completed their phase-based objectives and are no longer under active development. Examples include websites developed for one-time large-scale events or analysis tools used in completed research projects. These projects are highly unlikely to receive major future updates. Tier 0 may apply to projects with only a single contributor, while Tier 1 may apply when occasional future updates are possible. | Clearly mark the project as “Archived” in the README file and on the project website. Source code and documentation remain publicly available for reference, academic research, or reuse by others, but no official support, frequent updates, or security guarantees are provided. Nevertheless, such projects may still hold value for reference and reuse by other organizations. |
| Tier 2: Official Long-Term Support | Critical systems that support core public services and have high strategic importance, such as tax filing systems, digital identity services, or public warning systems. | The government allocates recurring budgets and forms dedicated internal teams or commissions professional vendors to carry out continuous development, maintenance, and security updates. This represents the highest level of commitment, ensuring system stability and reliability. |
| Tier 3–4: Community Stewardship | Highly practical tools or platforms that have formed active user or contributor communities but are not classified as critical infrastructure, such as data visualization tools, internal project management templates, or government website design systems. | The government’s role shifts from “lead developer” to “community enabler.” Instead of writing all code, the government provides essential infrastructure, establishes clear governance rules, and encourages community members to take on primary maintenance and development responsibilities. |""",
    )
    text = replace_once(
        text,
        """The code repository should include key governance documents to set clear codes of conduct and expectations for all participants.

##### Core governance documents

This includes detailed guidance on how to submit code contributions, such as: how to open issues, how to submit pull requests via CONTRIBUTING.md, coding style requirements and requirements for including tests.
CONTRIBUTING.md

Clearly define a community code of conduct to ensure a respectful, inclusive and professional collaborative environment.
CODE_OF_CONDUCT.md

Governance model documentation（GOVERNANCE.md）
Describe the project’s decision-making processes, as well as the roles and responsibilities of the primary maintainers.

All bug reports, feature proposals and technical discussions should be conducted through a public issue-tracking system.
Issue tracking

All code contributions must be reviewed by at least one maintainer to verify architectural soundness, coding style, and security standards before being merged into the main fork.
Code review""",
        """The code repository should include key governance documents to set clear codes of conduct and expectations for all participants.

##### Core governance documents

| Element | Description |
| --- | --- |
| CONTRIBUTING.md | Provides detailed guidance on how to submit code contributions, such as how to open issues, how to submit pull requests, coding style requirements, and requirements for including tests. |
| CODE_OF_CONDUCT.md | Defines a community code of conduct to ensure a respectful, inclusive, and professional collaborative environment. |
| GOVERNANCE.md | Describes the project’s decision-making processes, as well as the roles and responsibilities of the primary maintainers. |
| Issue tracking | All bug reports, feature proposals, and technical discussions should be conducted through a public issue-tracking system. |
| Code review | All code contributions must be reviewed by at least one maintainer to verify architectural soundness, coding style, and security standards before being merged into the main branch. |""",
    )

    text = replace_once(
        text,
        """Four Key Areas for Log Management
Structured Logging
Centralized Collection
Aggregate logs from different servers and services into a single platform to facilitate searching and analysis.
Use JSON or standardized formats to enable automated parsing and comparison by systems.
Compliance and Auditing
Real-Time Search and Analysis
Quickly locate specific errors or patterns, such as sources of abnormal traffic.
Retain necessary log records to meet security and legal requirements (e.g., GDPR, ISO 27001).""",
        """##### Four Key Areas for Log Management

| Area | Description |
| --- | --- |
| Structured logging | Use JSON or standardized formats to enable automated parsing and comparison by systems. |
| Centralized collection | Aggregate logs from different servers and services into a single platform to facilitate searching and analysis. |
| Compliance and auditing | Retain necessary log records to meet security and legal requirements (e.g., GDPR, ISO 27001). |
| Real-time search and analysis | Quickly locate specific errors or patterns, such as sources of abnormal traffic. |""",
    )
    text = replace_section(
        text,
        "#### 4.1.4 Information Security Management {#4-1-4-information-security-management}",
        "#### 4.1.5 Functional Maintenance {#4-1-5-functional-maintenance}",
        """

Information security management refers to protecting system resources and data confidentiality, integrity and availability through a combination of policies, technologies and processes. Common measures include identity authentication, access control, data encryption, intrusion detection, firewall configuration, vulnerability scanning and log auditing. These measures prevent unauthorized access, malicious attacks and data breaches while ensuring that the system can detect, respond to and recover from security threats.

![Key elements of information security management](assets/en-image1.png)

""",
    )
    text = replace_once(
        text,
        """Open-Source Software Issue Tracking and Resolution Workflow

Discussion and Additional Information
Categorization and Labeling
Create an Issue
Release and Documentation
PR Review and Merger
Fix and Submit a PR
Users or developers submit issues in the project’s issue tracker. The issue should include a title, description, reproduction steps, expected results and actual results.
Project maintainers label issues based on their nature (e.g., bug, question, security) and assign them to the relevant developers or teams.
Developers and community members can comment under the issue to clarify details, provide reproduction methods or suggest solutions.
Developers fix the code based on the issue and submit a Pull Request (PR), typically linking it to the corresponding issue (e.g., Fixes #123).
Maintainers review the PR to ensure correctness then merge it into the main fork and close the related issue.
The fix is included in the next release and recorded in the changelog for user reference.""",
        """##### Open-Source Software Issue Tracking and Resolution Workflow

| Step | Description |
| --- | --- |
| Create an issue | Users or developers submit issues in the project’s issue tracker. The issue should include a title, description, reproduction steps, expected results and actual results. |
| Categorization and labeling | Project maintainers label issues based on their nature (e.g., bug, question, security) and assign them to the relevant developers or teams. |
| Discussion and additional information | Developers and community members can comment under the issue to clarify details, provide reproduction methods or suggest solutions. |
| Fix and submit a PR | Developers fix the code based on the issue and submit a Pull Request (PR), typically linking it to the corresponding issue (e.g., Fixes #123). |
| PR review and merge | Maintainers review the PR to ensure correctness, merge it into the main branch, and close the related issue. |
| Release and documentation | The fix is included in the next release and recorded in the changelog for user reference. |""",
    )
    text = replace_once(
        text,
        """Create a fork
（Branch）
Develop and commit
Push to GitHub
（Push）
Create an issue

Create a PR
（Pull Request）
Tag and release version
Merge PR
Code Review""",
        """1. Create a branch
2. Develop and commit
3. Push to GitHub
4. Create an issue
5. Create a PR
6. Code review
7. Merge PR
8. Tag and release version""",
    )
    text = replace_once(
        text,
        """Open-Source Software Sustainability Strategy
Open-source talent development and culture building.
Community activity monitoring and continuous integration.
Establishment of system management and upgrade strategies.
License management and code reuse.
Connecting communities and public code platforms.""",
        """##### Open-Source Software Sustainability Strategy

- Open-source talent development and culture building.
- Community activity monitoring and continuous integration.
- Establishing system management and upgrade strategies.
- License management and code reuse.
- Connecting communities and public code platforms.""",
    )

    text = final_repairs(normalize_blank_lines(text), "en")
    path.write_text(text, encoding="utf-8")


def main() -> None:
    fix_zh()
    fix_en()


if __name__ == "__main__":
    main()
