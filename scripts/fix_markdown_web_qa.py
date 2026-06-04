from __future__ import annotations

import re
from pathlib import Path


ROOT = Path(__file__).resolve().parents[1]


def replace_block(text: str, old: str, new: str) -> str:
    if old not in text:
        return text
    return text.replace(old, new, 1)


def replace_section(text: str, start: str, end: str, new_body: str) -> str:
    start_idx = text.find(start)
    if start_idx == -1:
        return text
    body_start = start_idx + len(start)
    end_idx = text.find(end, body_start)
    if end_idx == -1:
        return text
    return text[:body_start] + new_body + text[end_idx:]


def fix_en() -> None:
    path = ROOT / "EN.md"
    text = path.read_text(encoding="utf-8")
    en_origin = """<a id="origin"></a>
### Origin

In an era of flourishing information technology, rapid development in big data and artificial intelligence, and increasingly strict information-security and risk-management requirements, public agencies face rising demands in information-system development and maintenance. These systems must improve internal administrative and operational efficiency while providing the public with more convenient digital services. At the same time, public-sector IT teams often face limited staffing and slower technological innovation. Against this backdrop, open-source software and Public Code offer new possibilities for change.

Open-source software is a development and licensing model contrasted with proprietary software. In common software-system procurement, an agency defines its business needs, selects a product or tool that already provides the core functions, asks a vendor to customize and deploy it, and pays through buy-out, licensing, or subscription models. After go-live, the agency usually obtains only the right to use the system.

Under the proprietary-software model, the source code is not public, licensing is provided by the original vendor, and agencies typically continue relying on that vendor for maintenance services, which also raises switching costs.

| Type | Source Code | Licensing and Support | User Rights |
| --- | --- | --- | --- |
| Proprietary software | Not public | Licensing provided by the original vendor | Right to use |
| Open-source software | Publicly available | Technical support may come from vendors, communities, or multiple providers | Ownership and reuse flexibility |

The core feature of open-source software is that its source code is publicly available and allows others to use, copy, modify, distribute, and share the technology. Procurement of open-source software systems focuses on establishing collaborative relationships among developers, vendors, and communities. Through this model, agencies can obtain technical support, integration services, and long-term maintenance capabilities while reducing licensing costs, avoiding vendor lock-in, improving technical autonomy and flexibility, and accelerating innovation through global community resources.

At the same time, Public Code echoes the spirit of open-source software. Originating in Europe and later expanding in countries such as the United States and Canada, Public Code follows the principle of “public money, public code.” It encourages the public sector to release source code developed or procured with public budgets under open-source licenses. Public Code can be understood as the public sector’s open-source software repository. It allows agencies with similar needs to reuse existing work, reduces duplicated manpower, budget, and time, and enables the public to inspect the quality of digital services. When services involve the public interest, transparent Public Code helps people understand how systems operate, builds trust, strengthens civic participation, and reinforces national digital infrastructure.

Therefore, the Ministry of Digital Affairs prepared this manual to help agencies understand open-source software and Public Code. The manual assists information-planning personnel in establishing management measures and standards for open-source software, and helps project owners, IT developers, and maintenance teams understand methods for adopting open-source software. In doing so, agencies can respond to international digital-development trends and gradually expand the use of open-source software.

![Preface illustration](assets/en-image6.png)"""
    text = re.sub(
        r'<a id="origin"></a>\n### Origin\n\n.*?\n!\[Preface illustration\]\(assets/en-image6\.png\)',
        en_origin,
        text,
        count=1,
        flags=re.DOTALL,
    )
    text = text.replace("Richard Stallman1", "Richard Stallman[^1]")
    text = text.replace("GNU2", "GNU[^2]")
    text = text.replace("Eric Raymond3’", "Eric Raymond[^3]’")
    text = text.replace("The Cathedral and the Bazaar4", "The Cathedral and the Bazaar[^4]")
    text = text.replace("TensorFlow11", "TensorFlow[^11]")
    text = text.replace("W3Techs in November[^7]", "W3Techs in November 2025[^7]")
    text = text.replace("copyleft15", "copyleft[^15]")
    text = text.replace("Boost Library21", "Boost Library[^21]")
    text = text.replace("“Security Considerations When Coding in the Open”23", "“Security Considerations When Coding in the Open”[^23]")
    text = text.replace("Standard for Public Code28", "Standard for Public Code[^28]")
    text = text.replace("Open-Source Definition（OSD）", "Open-Source Definition (OSD)")
    text = text.replace("Mozilla Public License（MPL） v2", "Mozilla Public License (MPL) v2")
    text = text.replace("OpenChain,s an ISO/IEC international standard", "OpenChain is an ISO/IEC international standard")
    text = text.replace("Github", "GitHub")
    text = text.replace("e.nsure", "ensure")
    text = text.replace("Ihe requirements", "The requirements")
    text = text.replace("grudually", "gradually")
    text = text.replace("3. nventory", "3. Inventory")
    text = text.replace("forbit hardcoding", "forbid hardcoding")
    text = text.replace("all bus are shallow", "all bugs are shallow")
    text = text.replace("Waves all copyright.", "Waives all copyright.")
    text = text.replace("Open-source Software and Public Cod", "Open-Source Software and Public Code")
    text = text.replace("flexibilitynd customization", "flexibility and customization")
    text = text.replace("officework and collaborative platform", "office work and collaborative platform")
    text = text.replace("Soverign Workplace", "Sovereign Workplace")
    text = text.replace("ZenDis", "ZenDiS")
    text = text.replace("ZenDis", "ZenDiS")
    text = text.replace("\nIntroduction to Open-Source Software\n\n<a id=\"chapter-1-introduction-to-open-source-software\"></a>", "\n<a id=\"chapter-1-introduction-to-open-source-software\"></a>")
    text = text.replace("*Image Source： openDesk.eu", "*Image source: openDesk.eu*")
    text = text.replace("*Resource：https://obamawhitehouse.archives.gov/sites/default/files/omb/memoranda/2016/m_16_21.pdf", "*Resource: https://obamawhitehouse.archives.gov/sites/default/files/omb/memoranda/2016/m_16_21.pdf*")
    text = text.replace("*image source： X-Road", "*Image source: X-Road*")
    text = text.replace("*image source：The repo-scaffolder project under DSACMS in the United States", "*Image source: The repo-scaffolder project under DSACMS in the United States*")
    text = text.replace("*image source： Grafana.com", "*Image source: Grafana.com*")

    replacements = {
        "[^1]: - Chapter:Introduction to Open-Source Software": "[^1]: Richard Stallman: Founder of the Free Software Foundation. He also launched the GNU Project and the Free Software Foundation, which later brought tremendous changes to the computer world.",
        "[^2]: - Chapter:Open-Source Software Application Evaluation": "[^2]: GNU: A recursive acronym for “GNU is Not Unix”. A recursive acronym is one that refers to itself, creating a humorous, self-referential loop, a tradition started among hackers in the early days, especially at MIT.",
        "[^3]: - Chapter:Open-Source Software Implementation": "[^3]: Eric Raymond: Generally recognized as one of the main leaders for the open-source movement since 1997. He is also one of the founders of the Open-Source Initiative.",
        "[^4]: - Chapter:Open-Source Software Maintenance and Operations": "[^4]: The Cathedral and the Bazaar: These are two different development models for free software. Under the Cathedral Model, the software is managed and monitored by a dedicated team. Under the Bazaar Model, the software is made public during its development, allowing public collaboration for fast correction and rapid releases.",
    }
    for old, new in replacements.items():
        text = text.replace(old, new)

    text = replace_block(
        text,
        """Source code: Not public

Vendor provides licensing
Proprietary Software
Users have the
“right to use”

Source code:
Available to the public

Technical support from non-specific vendor
Open-source
Software

Users have “ownership”""",
        """| Type | Source Code | Licensing and Support | User Rights |
| --- | --- | --- | --- |
| Proprietary software | Not public | Licensing provided by the original vendor | Right to use |
| Open-source software | Publicly available | Technical support may come from vendors, communities, or multiple providers | Ownership and reuse flexibility |""",
    )
    text = replace_block(
        text,
        """Four Freedoms of Free Software

The freedom to run the program as you wish, for any purpose.
The freedom to study how the program works, and change it so it does your computing as you wish.
The freedom to redistribute copies so you can help your neighbor.
The freedom to distribute copies of your modified versions to others. By doing this you can give the whole community a chance to benefit from your changes.
Freedom 0
Freedom 1
Freedom 2
Freedom 3""",
        """The Four Freedoms of Free Software can be summarized as follows:

| Freedom | Meaning |
| --- | --- |
| Freedom 0 | The freedom to run the program for any purpose. |
| Freedom 1 | The freedom to study how the program works and change it to meet your needs. |
| Freedom 2 | The freedom to redistribute copies to help others. |
| Freedom 3 | The freedom to distribute modified versions so the whole community can benefit. |""",
    )
    text = replace_block(
        text,
        """The Cathedral Model
The Bazaar Model

Open/
distributed development

![Cathedral model illustration](assets/en-image8.png)

![Bazaar model illustration](assets/en-image7.jpeg)

Closed/
centralized development

Source code allows
public participation
Source code maintained
by the developers

Frequent updates with a
focus on rapid iteration

Slower updates with a focus on order""",
        """The essay contrasts two development models:

| Model | Development Style | Source Code and Release Pattern |
| --- | --- | --- |
| Bazaar model | Open and distributed development | Source code is open to public participation, with frequent releases and rapid iteration. |
| Cathedral model | Closed and centralized development | Source code is maintained by a dedicated developer group, with slower releases and greater emphasis on order. |

![Cathedral model illustration](assets/en-image8.png)

![Bazaar model illustration](assets/en-image7.jpeg)""",
    )
    text = replace_block(
        text,
        """“Free” is easily misunderstood as “free of charge” instead of “freedom to use.”
The narrative behind it has highly political and centers on ethics, which some businesses worry can be considered “anti-business.”""",
        """- “Free” is easily misunderstood as “free of charge” instead of “freedom to use.”
- The narrative has a strong ethical and political framing, which some businesses worry may be perceived as “anti-business.”""",
    )
    text = replace_block(
        text,
        """Open-Source Definition (OSD)

Free Distribution
Source Code
Derived Works
Integrity of The Author’s Source Code

No Discrimination Against Persons or Groups

No Discrimination Against Fields of Endeavor

Distribution of License
License Must Not Be
Specific to a Product

License Must Not
Restrict Other Software

License Must Be Technology-Neutral
The software should be free to sell or give away without needing to pay the licensing fee.
The program must include source code and must allow distribution in source code as well as compiled form.
The license must allow modifications and derived works and must allow them to be distributed.
The license may restrict source-code from being distributed in modified form only if the license allows the distribution of “patch files” and must explicitly permit distribution of software built from modified source code.
The license must not discriminate against any person or group of persons.
The license must not restrict anyone from making use of the program in a specific field of endeavor (such as business or research)
The program is redistributed without the need for execution of an additional license.
The rights attached to the program must not depend on the program’s being part of a particular software distribution.
The license must not insist that all other programs distributed on the same medium must be open-source software.
No provision of the license may be predicated on any individual technology or style of interface""",
        """The Open-Source Definition (OSD) can be summarized in ten requirements:

| Requirement | Explanation |
| --- | --- |
| Free distribution | The software may be sold or given away without requiring a license fee. |
| Source code | The program must include source code and allow distribution in both source-code and compiled forms. |
| Derived works | The license must allow modifications, derived works, and redistribution. |
| Integrity of the author’s source code | The license may require modified versions to be distributed as patch files, but it must still allow distribution of software built from modified source code. |
| No discrimination against persons or groups | The license must not exclude any person or group. |
| No discrimination against fields of endeavor | The license must not restrict use in specific fields such as business or research. |
| Distribution of license | Redistribution must not require an additional license agreement. |
| License not specific to a product | Rights must remain in effect even when the software is separated from the original distribution. |
| License must not restrict other software | The license must not require other software on the same medium to also be open source. |
| Technology-neutral | The license must not depend on a specific technology or interface. |""",
    )
    text = replace_block(
        text,
        """openDesk is more than a collaborative tool. It is a part of the realization of the digital sovereignty policy, which means it can:
Reduce vendor lock-in: If the government over-relies on a specific commercial software provider (especially a major corporation from other countries), it will lose control in so many levels, such as data access, maintenance, upgrade, privacy and oversight. openDesk adopts open source and an open standard, emphasizing its interoperability and interchangeability, freeing government agencies from vendor lock-in.

Enhance transparency and security: Open-source software comes with open source code for inspection, which is very important to government agencies as it can help them find loopholes/backdoors. Open source code also makes it easier for a third party to review the software, which means more transparency and higher legal/oversight accountability.
Unified and standardized: With a unified collaborative platform, it reduces the extra workload, training cost and maintenance cost from multiple small tools at various locations. This will also enhance administrative efficiency and inter-department collaboration. openDesk strives to provide a consistent user interface and user experience.
Policy and legal support: The promotion of openDesk echoes with the German government’s digital strategy, IT-Planungsrat[^14] and “Digital Sovereignty” policy, which encourage government agencies to adopt open-source software to ensure their autonomy and flexibility.""",
        """openDesk is more than a collaboration tool. It is part of Germany’s digital sovereignty policy and has the following implications:

- Reduce vendor lock-in: When government agencies over-rely on a single commercial software provider, especially a major foreign vendor, they lose control over data access, maintenance, upgrades, privacy, and oversight. openDesk adopts open source and open standards to emphasize interoperability and replaceability.
- Enhance transparency and security: The source code can be inspected, which helps agencies identify vulnerabilities or backdoors and makes third-party review easier.
- Unify and standardize workflows: A unified collaboration platform reduces the operational burden, training cost, and maintenance cost caused by scattered tools, while improving administrative efficiency and interdepartmental collaboration.
- Support policy and legal goals: The promotion of openDesk echoes the German government’s digital strategy, IT-Planungsrat[^14], and Digital Sovereignty policy, which encourage government agencies to adopt open-source software to preserve autonomy and flexibility.""",
    )
    text = replace_block(
        text,
        """Five Digital Public Goods in the UN’s “Secretary-General’s Roadmap for Digital Cooperation”

Open
Content
Open
Standards
Open Artificial Intelligence
Open Data""",
        """The five Digital Public Goods in the UN’s “Secretary-General’s Roadmap for Digital Cooperation” are:

- Open data
- Open-source software
- Open content
- Open standards
- Open artificial intelligence models""",
    )
    text = replace_block(
        text,
        """Copyright Protection
Strength
Permissive
Strong
Files containing source code under LGPL license does not need to go open source.
Anyone who modifies, integrates and merges the source code under GPL license must be released under the same license when go open source.
Any web service using source code from AGPL-licensed files must publish its entire source code.""",
        """The GPL family can be understood by the strength of its copyleft obligations:

| License | Copyleft Strength | Core Obligation |
| --- | --- | --- |
| AGPL | Strongest | Web services using AGPL-licensed source code must publish the complete corresponding source code. |
| GPL | Strong | Modified or integrated GPL source code must be released under the same license when distributed. |
| LGPL | Weaker | Files that only use LGPL-licensed code through a library interface generally do not require the entire project to be open sourced. |""",
    )
    text = replace_block(
        text,
        """Strict
Copyright Protection
Level
Permissive
Any software built upon modified GPL code or incorporating GPL code must be licensed under GPL.
There are variants including AGPL, GPL and LGPL.
The source code of a file must be made public if the file is modified and licensed under MPL V2.
Requires that both copyright and license notices be included and that contributors involved must explicitly grant the copyright.
Only requires that both copyright and license notices be included when distributing the source code.
Only requires that the copyright notice and license text must be included when distributing the source code (does not apply to the edited binary file)
Waives all copyright.""",
        """The six licenses introduced above can also be placed on a spectrum from strict copyleft to permissive licensing:

| License Type | Requirement |
| --- | --- |
| AGPL / GPL / LGPL | The GPL family requires corresponding open-source release under the same license when its copyleft conditions are triggered. |
| MPL v2 | If an MPL-licensed file is modified, the source code of that file must be made public. |
| Apache License v2 | Requires copyright and license notices, and contributors explicitly grant patent rights. |
| MIT License | Requires copyright and license notices when distributing the source code. |
| Boost Software License 1.0 | Requires copyright and license text when distributing source code, but not when distributing compiled binaries. |
| The Unlicense | Waives copyright and releases the work into the public domain. |""",
    )
    text = replace_block(
        text,
        """Supporting Measures
Mission
Target
Open-Source Software and Public Code

Source code from software developed/procured by each agency
Public Code Platform
code.gov.tw

Public Money
Public Code
Manual for Open-Source Software Applications for Government Agencies

Business Model

People, Process, Technology

Public Code

A series of courses on public code and open source

Use
Essential Principles

With License
Agreement

Commercial use
Public Access

Non-profit use
Allow Use

Allow Copying

Allow Modification

Allow Distribution""",
        """The relationship between open-source software and Public Code can be summarized as follows:

| Aspect | Public-Code Focus |
| --- | --- |
| Mission | Apply the principle of “public money, public code” to software developed or procured by government agencies. |
| Target | Release source code through public-code platforms such as `code.gov.tw`. |
| Supporting measures | Provide manuals, training, governance models, and technical support for agencies and project teams. |
| Basic principles | Allow public access, use, copying, modification, distribution, and use under open-source licenses for both commercial and non-profit purposes. |""",
    )
    text = text.replace("\nOpen-Source Software Application Evaluation\n\nIn the planning process", "\nIn the planning process")
    text = text.replace("\nSector Open-Source Software Playbook\n\n## Notes", "\n\n## Notes")
    text = replace_block(
        text,
        """Main Differences Between Proprietary and Open-source Software
Proprietary
Open-Source
| Software and service costs | Software licensing fee Technical support fee | Mainly just the technical support fee. |
| --- | --- | --- |
Financial Cost
Security Manag-ement
| Source code transparency | Kept secret and maintained by the developing company | Completely accessible to the public for review and verification of its security. |
| --- | --- | --- |
| Vulnerability patching Mechanism | The developing company will schedule the security checks and vulnerability patching updates | With the community close oversight, it will have frequent updates. The agency should pay close attention to the community and establish a maintenance process. |
| Supplier Collaboration | Works with one single company, usually the original manufacturer or an authorized distributor | Work with one or multiple companies for the project. Less restriction while selecting the companies. |
| --- | --- | --- |
| System Integration | Usually adopts the open standard with higher system integration flexibility and customization depends on the product’s API or protocol | Usually adopts the open standard with higher system integration flexibility. |
Implem-entation Model
License Manage-ment
| License | Exclusive license with restricted scope of use. | Open license permitting modification and redistribution. |
| --- | --- | --- |
| Restrictions | Protected by the copyright law, a licensing agreement specifies the restrictions in the use of the software. Reverse engineering is usually prohibited. | One system may involve the management of multiple licenses. Therefore, it is needed to verify the compatibility between multiple open-source licenses. |""",
        """The main differences between proprietary and open-source software are as follows:

| Dimension | Item | Proprietary Software | Open-Source Software |
| --- | --- | --- | --- |
| Financial cost | Software and service costs | Software licensing fees and technical support fees. | Mainly technical service costs. |
| Security management | Source-code transparency | Source code is not public and is maintained by the vendor. | Source code is usually public and can be reviewed by communities and the public. |
| Security management | Vulnerability patching | Security checks and patches are scheduled by the vendor. | Community oversight is strong and updates are frequent; agencies must monitor community activity and establish maintenance processes. |
| Implementation model | Supplier collaboration | Usually involves one vendor, such as the original vendor or an authorized distributor. | A project may work with one or multiple vendors, with fewer restrictions on vendor selection. |
| Implementation model | System integration | Integration and customization depend on the product’s API or protocol. | Open standards are commonly used, providing greater integration flexibility. |
| License management | License model | Proprietary licenses restrict the scope of use. | Open licenses allow modification and redistribution. |
| License management | Use restrictions | Protected by copyright law and licensing contracts, usually prohibiting reverse engineering. | A single system may involve multiple open-source licenses and requires license-compatibility review. |""",
    )
    text = replace_section(
        text,
        '<a id="2-2-1-open-source-software-benefits"></a>\n#### 2.2.1 Open-Source Software Benefits\n\n',
        '\n<a id="2-2-2-risk-analysis-of-open-source-software"></a>',
        """When the public sector uses open-source software for information-system development, it is not only practicing open and transparent digital governance; it also gains clear benefits in cost, security, customization, system integration, vendor choice, and policy value.

| Benefit | Explanation |
| --- | --- |
| Policy and public value | Choosing open source is both a technical choice and a policy statement: digital tools should serve the public interest, improve transparency and auditability, and strengthen public trust. |
| Predictable financial cost | Open-source software has no licensing fees, and agencies retain fairer bargaining power over future maintenance fees. |
| Vendor flexibility | Agencies are not locked into a designated vendor and may choose local or international providers, reducing vendor-lock-in risk and encouraging industry development. |
| Security-management autonomy | Public source code helps agencies understand and control systems; communities and third parties can identify and fix vulnerabilities earlier. |
| System integration | Open-source software often adopts standard protocols and formats, making it easier to integrate with existing systems and support cross-platform collaboration. |
| Customization | Agencies may modify functions, expand modules, and optimize interfaces according to business processes. |
""",
    )
    text = replace_section(
        text,
        '<a id="2-2-2-risk-analysis-of-open-source-software"></a>\n#### 2.2.2 Risk Analysis of Open-Source Software\n\n',
        '\n<a id="2-3-open-source-software-implementation-model"></a>',
        """Even though open-source software offers significant benefits, agencies should still conduct a complete risk assessment during system adoption. This process may be integrated with existing risk-management activities: (1) collect risk issues related to software currently used or planned for adoption; (2) evaluate each risk by likelihood and impact; and (3) prepare response measures for risks whose scores exceed acceptable thresholds.

Common risks include:

| Risk | Description |
| --- | --- |
| Transition risk | Migrating from proprietary software to open-source software may require substantial manpower and time for data migration, process redesign, system validation, and staff training. |
| Vendor quality and maintenance responsibility | Open-source projects may rely on community support; public-sector systems still require reliable development and maintenance teams, clear responsibility, and stable vendor quality. |
| Information-security risk | Agencies must establish security monitoring and patching mechanisms so systems are not exposed to known vulnerabilities. |
| Licensing and legal risk | Open-source licenses such as GPL, MIT, and Apache are legally binding. Agencies should review license compatibility and consult legal advisors when necessary. |
| User acceptance | Staff may be accustomed to proprietary tools such as Microsoft Office or Google Workspace; training and cultural change remain essential. |
""",
    )
    text = replace_section(
        text,
        '<a id="2-3-1-development-strategy-adopt-integrate-or-self-build"></a>\n#### 2.3.1 Development Strategy: Adopt, integrate or self-build?\n\n',
        '\n<a id="2-3-2-explore-projects-and-referenceable-platform"></a>',
        """When the public sector uses open-source software for information-system development, it should choose an implementation strategy according to project needs, internal capacity, and long-term governance requirements.

1. Adopt: When project requirements can be clearly mapped to mature open-source software, directly adopting the existing solution is efficient and relatively low risk. This approach can reduce implementation time and duplicated development, reuse global community experience, adopt open specifications and standards, and reduce maintenance challenges through public source code and community resources.

2. Integrate: This approach combines multiple open-source projects, such as frameworks, libraries, or data platforms, to form a flexible solution that meets local needs. Germany’s openDesk is an example: it integrates multiple existing open-source services into a sovereign office suite for German public agencies.

3. Self-build: For special requirements or critical and sovereign systems, agencies may need to build systems in-house to ensure legal compatibility, long-term maintenance flexibility, national-security requirements, digital sovereignty, or control over core government services.

Regardless of the strategy, successful open-source adoption depends on an “Open First” approach. Openness should be treated as a design principle from the beginning. Agencies should assume future open-source release early in the project and prepare the architecture, license management, and documentation accordingly. Components should remain closed only when necessary for security, privacy, or unreleased policy reasons. For layered design, agencies may refer to the UK government guideline “Security Considerations When Coding in the Open”[^23], which reminds us that “security should be designed into openness, not into secrecy.”

Open First security governance can be summarized as follows:

| Control | Practice |
| --- | --- |
| Key and certificate separation | Use a secure key-management system and avoid hardcoding certificates in source code. |
| Automated scanning and review | Incorporate automated tools into version control to detect sensitive data and potential risks. |
| Responsible vulnerability reporting | Build an open, transparent, and safe mechanism for reporting vulnerabilities. |

""",
    )
    text = replace_block(
        text,
        """| Platform | Operator | Features | Famous Projects |
| --- | --- | --- | --- |
| Software Index
openCode.de | The Centre for Digital Sovereignty (ZenDiS) of Germany | Focuses on digital sovereignty and compliance in the EU, with an emphasis on reusability and continued maintenance | OpenDesk (refer to [1.2.2](#1-2-2-un-proposes-digital-public-goods) of this Manual) FIM (Federated Information Management) Smart Village App (a local governance application). |
| SILL database
code.gouv.fr | The Interministerial Digital Directorate (DINUM) of France | Integrates the free software adopted and maintained by different ministries. | LiiBRE (open-source office environment solution) OpenFisca (social policy simulation tool) GeoNature (ecosystem observation and geoinformation system). |

| Platform | Operator | Features | Famous Projects |
| --- | --- | --- | --- |
| DGPs Entrance
Digital Public Goods Registry | Digital Public Goods Alliance (DPGA) of the UN, jointly maintained by UNICEF, UNDP and Norad | Focuses on open-source software that can promote SDGs, with each project required to pass the open-source, ethical, governance and transparency review. | DHIS2 (public health information platform) OpenCRVS (civil registration system) U-Report (youth civic participation platform) |
| Public Code Platform Code.gov.tw | Ministry of Digital Affairs (MoDA) of Taiwan | The Taiwan government has gradually established this public code platform that integrates open-source projects and API and promotes interdepartmental collaboration and open governance. | Data safe transfer verification system Standard address writing API Codefest Taipei website |""",
        """| Platform | Operator | Features | Representative Projects |
| --- | --- | --- | --- |
| Software Index openCode.de | Germany’s Centre for Digital Sovereignty (ZenDiS) | Focuses on digital sovereignty and EU compliance, with an emphasis on reuse and sustainable maintenance. | openDesk, FIM (Federated Information Management), Smart Village App. |
| SILL database code.gouv.fr | France’s Interministerial Digital Directorate (DINUM) | Integrates free software adopted and maintained by ministries. | LiiBRE, OpenFisca, GeoNature. |
| Digital Public Goods Registry | Digital Public Goods Alliance (DPGA), jointly maintained by UNICEF, UNDP, and Norad | Focuses on open-source software that promotes the SDGs; each project must pass open-source, ethical, governance, and transparency review. | DHIS2, OpenCRVS, U-Report. |
| Public Code Platform Code.gov.tw | Ministry of Digital Affairs (MoDA), Taiwan | Integrates open-source projects and APIs, and promotes interdepartmental collaboration and open governance. | Data Safe Transfer Verification System, Standard Address Writing API, CodeFest Taipei website. |""",
    )
    text = replace_block(
        text,
        """Supply chain
blind spots
Version and maintenance risks
Licensing risks
When a vendor fails to disclose all the open-source components that it utilizes, an agency will not have the complete software bill of materials it uses. Once there is a vulnerability from one of these open-source components, the agency will not be able to respond in time.
Different systems using different versions of the same open-source component will constitute to maintenance difficulties and potential conflicts in the long term within the agency
With multiple open-source licenses (such as GPL, Apache and MIT), failure to comply with the licensing terms may lead to legal disputes or forced publication of the entire system""",
        """| Risk | Explanation |
| --- | --- |
| Supply-chain blind spots | If vendors do not disclose all open-source components, agencies cannot maintain a complete software bill of materials and may be unable to respond quickly when upstream vulnerabilities appear. |
| Version and maintenance risk | Different systems using different versions of the same open-source component may create long-term maintenance difficulty and internal conflicts. |
| Licensing risk | Open-source licenses are diverse; failure to comply with obligations under GPL, Apache, MIT, and other licenses may cause legal disputes or require source-code release. |""",
    )
    text = text.replace("projects.d", "projects.")
    text = re.sub(r"^(\[\^\d+\]: [^:\n]+):(?!\s)", r"\1: ", text, flags=re.MULTILINE)
    path.write_text(text, encoding="utf-8")


def fix_zh() -> None:
    path = ROOT / "ZH_TW.md"
    text = path.read_text(encoding="utf-8")
    text = text.replace("| V1.1 | 初版修改（完稿第一版）| 97 |", "| V1.1 | 初版修改（完稿第一版） | 97 |")
    text = text.replace("GNU 計畫 。", "GNU 計畫。")
    text = text.replace("四大自由 與", "四大自由與")
    text = text.replace("IT- 規劃委員會", "IT 規劃委員會")
    text = text.replace("Open Culture Foundation，下簡稱 OCF）", "Open Culture Foundation，以下簡稱 OCF）")
    text = text.replace("Hadoop[^16] 、Spark[^17] 、Kubernetes[^18]", "Hadoop[^16]、Spark[^17]、Kubernetes[^18]")
    text = text.replace("Node.js[^19] 、Ruby on Rails[^20]", "Node.js[^19]、Ruby on Rails[^20]")
    text = text.replace("丹麥 OS2 聯盟（Offentligt Software Samarbejde25）", "丹麥 OS2 聯盟[^25]（Offentligt Software Samarbejde）")
    text = text.replace("《 程式碼何時應開放或封閉》", "《程式碼何時應開放或封閉》")
    text = text.replace("聯合國《秘書長數位合作路線圖 》", "聯合國《秘書長數位合作路線圖》")
    text = text.replace("參考聯盟網址：https://floss-pso.network/ 。", "參考聯盟網址：https://floss-pso.network/。")
    text = text.replace("財團法人開放文化基金會 Open Culture Foundation，以下簡稱 OCF）", "財團法人開放文化基金會（Open Culture Foundation，以下簡稱 OCF）")
    text = text.replace("6 種授權條款開始介紹 。", "6 種授權條款開始介紹。")
    text = text.replace("像是 「Choose an Open-Source license」", "像是「Choose an Open-Source license」")
    text = text.replace("（例如： Node.js", "（例如：Node.js")
    text = text.replace("社群廣泛採用 。", "社群廣泛採用。")
    text = text.replace("已知漏洞 。", "已知漏洞。")
    text = text.replace("tag-value 。", "tag-value。")
    text = text.replace("JSON, XML 。", "JSON, XML。")
    text = text.replace("許多國家 僅", "許多國家僅")
    text = text.replace("ISO/IEC 18974 標準 。", "ISO/IEC 18974 標準。")
    text = text.replace("CVE 資料庫的漏洞 。", "CVE 資料庫的漏洞。")
    text = text.replace("參考[附錄四]", "參考 [附錄四]")
    text = text.replace("本手冊[附錄五]", "本手冊 [附錄五]")
    text = text.replace("如:", "如：")
    text = text.replace("Github", "GitHub")
    text = text.replace("常見於CONTRIBUTING.md文件中", "常見於 CONTRIBUTING.md 文件中")
    text = text.replace("Apache 2.0授權條款", "Apache 2.0 授權條款")
    text = text.replace("NOTICE文件", "NOTICE 文件")
    text = text.replace("可以透過SBOM", "可以透過 SBOM")
    text = text.replace("[4.2](#4-2-sustainable-operations).2 定期檢視開源專案的維護狀況與社群活躍度", "[4.2.2](#4-2-2-community-activity-monitoring-and-continuous-integration) 定期檢視開源專案的維護狀況與社群活躍度")
    text = text.replace("產生衝突.[4.2.2](#4-2-2-community-activity-monitoring-and-continuous-integration) 定期檢視開源專案的維護狀況與社群活躍度，也有助於評估是否持續使用或尋找替代方案。", "產生衝突。另可參考 [4.2.2](#4-2-2-community-activity-monitoring-and-continuous-integration)「社群動態追蹤與持續整合」，評估是否持續使用或尋找替代方案。")
    text = text.replace("*圖片來源： openDesk.eu", "*圖片來源：openDesk.eu*")
    text = text.replace("*圖片來源：https://obamawhitehouse.archives.gov/sites/default/files/omb/memoranda/2016/m_16_21.pdf", "*圖片來源：https://obamawhitehouse.archives.gov/sites/default/files/omb/memoranda/2016/m_16_21.pdf*")
    text = text.replace("*CC By 4.0 “FLOSS-PSO 網絡地圖” 資料來源: OSPO 聯盟", "*CC By 4.0 “FLOSS-PSO 網絡地圖” 資料來源：OSPO 聯盟*")
    text = text.replace("*圖片來源： X-Road", "*圖片來源：X-Road*")
    text = text.replace("*圖片來源：美國 DSACMS 下轄 repo-scaffolder 專案", "*圖片來源：美國 DSACMS 下轄 repo-scaffolder 專案*")
    text = text.replace("*圖片來源： Grafana.com", "*圖片來源：Grafana.com*")
    toc_start = text.index("## 目錄")
    next_anchor = text.index('<a id="introduction"></a>')
    toc = """## 目錄

- [緒論](#introduction)
- [第一章 開源軟體介紹](#chapter-1-introduction-to-open-source-software)
  - [1.1 開源軟體發展背景](#1-1-how-it-started)
  - [1.2 開源軟體國際趨勢與應用](#1-2-international-trends-and-applications)
  - [1.3 開源軟體基本概念與授權條款類型](#1-3-basic-concept-and-licensing-agreement-types-of-open-source-software)
  - [1.4 開源軟體與公共程式](#1-4-open-source-software-and-public-code)
- [第二章 開源軟體應用評估](#chapter-2-open-source-software-application-evaluation)
  - [2.1 使用開源軟體及專有軟體差異說明](#2-1-difference-between-using-open-source-and-proprietary-software)
  - [2.2 開源軟體使用效益與風險評估](#2-2-open-source-software-benefits-and-risks-analysis)
  - [2.3 開源軟體導入模式](#2-3-open-source-software-implementation-model)
  - [2.4 開源軟體治理制度](#2-4-open-source-software-governance-system)
- [第三章 開源軟體導入方法](#chapter-3-open-source-software-implementation)
  - [3.1 軟體開發流程：需求與設計開源注意事項](#3-1-software-development-process-needs-and-cautions-when-designing-open-source-software)
  - [3.2 軟體開發流程：開發與測試開源注意事項](#3-2-software-development-process-considerations-for-open-source-during-development-and-testing)
  - [3.3 軟體開發流程：上線與驗收開源注意事項](#3-3-software-development-process-open-source-considerations-for-go-live-and-acceptance)
  - [3.4 將開發成果開源釋出](#3-4-releasing-development-outcomes-as-open-source)
- [第四章 開源軟體維護與營運](#chapter-4-open-source-software-maintenance-and-operations)
  - [4.1 開源軟體維運](#4-1-open-source-software-operations-and-maintenance)
  - [4.2 開源軟體永續經營](#4-2-sustainable-operations)
  - [4.3 結語](#4-3-conclusion)
- [附錄一 名詞解釋](#appendix-i-terminology)
- [附錄二 常見問答 FAQ](#appendix-ii-faq)
- [附錄三 參考資源](#appendix-iii-links)
- [附錄四 需求規劃自主檢核表](#appendix-iv-requirements-planning-self-assessment-checklist)
- [附錄五 授權合規評估檢核表](#appendix-v-license-compliance-assessment-checklist)

"""
    text = text[:toc_start] + toc + text[next_anchor:]
    text = replace_block(
        text,
        """原始碼不公開

原廠提供授權
專有軟體

使用者有「使用權」

原始碼公開

不特定廠商支援技術
開源軟體

使用者有「所有權」""",
        """| 類型 | 原始碼狀態 | 技術支援與授權 | 使用者取得 |
| --- | --- | --- | --- |
| 專有軟體 | 原始碼不公開 | 原廠提供授權 | 使用權 |
| 開源軟體 | 原始碼公開 | 可由不特定廠商或社群支援 | 所有權與再利用彈性 |""",
    )
    text = replace_section(
        text,
        '<a id="3-3-1-open-source-software-license-compliance-review-checklist-and-risk-management-recommendations"></a>\n#### 3.3.1 開源軟體授權合規檢核（表）與風險控管建議\n\n',
        '\n<a id="3-3-2-the-core-of-acceptance-transferability-readability-and-sustainability"></a>',
        """針對專案中採用的開源軟體，建議使用「公部門使用開源軟體（或公共程式）授權合規評估檢核表」作為檢核工具（可參考本手冊 [附錄五](#appendix-v-license-compliance-assessment-checklist)「公部門使用開源軟體（或公共程式）授權合規評估檢核表」）。表單內容主要包含專案基本資訊、檢核項目，以及開發成果作為公共程式等三大區塊，協助機關識別採用開源軟體的風險並規劃風險控管措施。

依據前述評估檢核表的填寫結果，可特別留意以下事項，以強化機關使用開源軟體的風險控管品質：

- 授權條款整合：若系統包含採用不同授權條款的程式碼，應留意各授權條款要求。例如，將 GPL 授權程式碼與 MIT 或 Apache 授權程式碼整合時，衍生作品須遵守 GPL「必須同樣採 GPL」之要求。
- 與專有軟體整合：若程式碼有整合至專有軟體的需求，須特別注意 GPL 屬於強制開放原始碼的授權；若整合到對外服務的閉源系統卻不開放源碼，可能違反授權。
- 上線後開源釋出及維運方式：若系統釋出作為公共程式，須規劃適當資源處理議題，持續關注社群動態，並建立版本升級機制與策略（詳見 [第四章](#chapter-4-open-source-software-maintenance-and-operations)）。
""",
    )
    text = replace_block(
        text,
        """自由軟體的四大自由

為了任何目的執行程式的自由。
研究程式如何運作的自由，並依需求修改程式。
再次散布程式的自由，以幫助他人。
改善程式的自由，並將這些改進回饋給社群。
自由之零
自由之一
自由之二
自由之三""",
        """自由軟體的四大自由可整理如下：

| 自由 | 內容 |
| --- | --- |
| 自由之零 | 為了任何目的執行程式的自由。 |
| 自由之一 | 研究程式如何運作的自由，並依需求修改程式。 |
| 自由之二 | 再次散布程式的自由，以幫助他人。 |
| 自由之三 | 改善程式的自由，並將這些改進回饋給社群。 |""",
    )
    text = replace_block(
        text,
        """市集模式
大教堂模式

![大教堂模式示意圖](assets/zh-tw-image8.png)

![市集模式示意圖](assets/zh-tw-image7.jpeg)

開放/分散式開發

封閉/集中式開發

原始碼公開供大眾參與

原始碼由開發者維護

更新頻繁，強調快速迭代

更新較慢，強調秩序""",
        """《大教堂與市集》所對比的兩種模式可整理如下：

| 模式 | 開發方式 | 原始碼與更新特性 |
| --- | --- | --- |
| 市集模式 | 開放、分散式開發 | 原始碼公開供大眾參與，更新頻繁，強調快速迭代。 |
| 大教堂模式 | 封閉、集中式開發 | 原始碼由開發者維護，更新較慢，強調秩序。 |

![大教堂模式示意圖](assets/zh-tw-image8.png)

![市集模式示意圖](assets/zh-tw-image7.jpeg)""",
    )
    text = replace_block(
        text,
        """英文中的 “Free” 容易被誤解為「免費」而非「自由」。
論述帶有倫理/政治色彩，部分企業擔心可能被視為「反商業」。""",
        """- 英文中的 “Free” 容易被誤解為「免費」而非「自由」。
- 論述帶有倫理／政治色彩，部分企業擔心可能被視為「反商業」。""",
    )
    text = replace_block(
        text,
        """開放原始碼定義（OSD）

軟體可自由銷售或贈送，不需支付授權費
須提供原始碼，且允許以原始碼或編譯後形式散布
授權必須允許修改與再散布
可要求修改版以補丁型式提供，但須允許散布修改後的程式
授權不得排除任何人
不得禁止在特定領域使用（如商業或研究）
再散布時不需額外簽署授權
軟體脫離原始發行版仍保有同樣權利
不得要求同媒介上的其他軟體也必須開源
授權不得依賴特定技術或介面
自由再散布
原始碼公開
允許衍生作品
維護原始碼完整性

不得歧視個人/群體

不得限制用途領域

授權隨軟體傳遞

授權不依附特定產品

不得限制其他軟體

技術中立""",
        """開放原始碼定義（OSD）可整理為下列十項要件：

| 要件 | 說明 |
| --- | --- |
| 自由再散布 | 軟體可自由銷售或贈送，不需支付授權費。 |
| 原始碼公開 | 須提供原始碼，且允許以原始碼或編譯後形式散布。 |
| 允許衍生作品 | 授權必須允許修改與再散布。 |
| 維護原始碼完整性 | 可要求修改版以補丁型式提供，但須允許散布修改後的程式。 |
| 不得歧視個人／群體 | 授權不得排除任何人。 |
| 不得限制用途領域 | 不得禁止在特定領域使用，例如商業或研究。 |
| 授權隨軟體傳遞 | 再散布時不需額外簽署授權。 |
| 授權不依附特定產品 | 軟體脫離原始發行版仍保有同樣權利。 |
| 不得限制其他軟體 | 不得要求同媒介上的其他軟體也必須開源。 |
| 技術中立 | 授權不得依賴特定技術或介面。 |""",
    )
    text = replace_block(
        text,
        """openDesk 不只是個協作工具，更是數位主權政策實踐的一部分，其意義包含：
減少對專有／單一供應商的依賴（Vendor Lock-In）：公部門如果過度依賴某一家商業軟體供應商（特別是境外的大型公司），就會在許多層面缺乏控制權利（例如資料存取、維護、升級、隱私、監管等）。openDesk 採用「開放原始碼」與「開放標準」，強調可互通性、可替換性，讓政府機構不被某個供應商綁死。
提升透明度與安全性：開源軟體其原始碼可檢查，對公部門尤其重要，有助於找到安全漏洞／後門。也容易被第三方審核。透明度高也有助於法律／監管的信任。
統一與標準化：通過統一的一套協作平臺，可減少多套／分散的小工具造成的操作負擔、訓練成本與維護成本。也利於行政效率和跨部門協作。 openDesk 在使用者介面與使用者體驗上也力求統一，。
政策與法律支持：openDesk 的推動呼應德國政府的數位策略、IT 規劃委員會（IT-Planungsrat[^14]）「Digital Sovereignty（數位主權）」政策，鼓勵公部門使用開源軟體以確保自主性與彈性。""",
        """openDesk 不只是協作工具，更是數位主權政策實踐的一部分，其意義包含：

- 減少對專有／單一供應商的依賴（Vendor Lock-In）：公部門若過度依賴單一商業軟體供應商，特別是境外大型公司，便可能在資料存取、維護、升級、隱私與監管等層面缺乏控制權。openDesk 採用開放原始碼與開放標準，強調可互通性與可替換性，避免政府機構被單一供應商綁定。
- 提升透明度與安全性：開源軟體的原始碼可被檢查，有助於發現安全漏洞或後門，也更容易接受第三方審核；透明度提升後，也有助於法律與監管層面的信任。
- 統一與標準化：統一的協作平臺可減少多套分散工具造成的操作負擔、訓練成本與維護成本，並提升行政效率與跨部門協作。openDesk 也在使用者介面與使用者體驗上追求一致性。
- 政策與法律支持：openDesk 的推動呼應德國政府的數位策略、IT 規劃委員會（IT-Planungsrat[^14]）「Digital Sovereignty（數位主權）」政策，鼓勵公部門使用開源軟體以確保自主性與彈性。""",
    )
    text = replace_block(
        text,
        """聯合國《秘書長數位合作路線圖》五大數位公共財

開放資料 開源軟體 開放內容 開放標準 開放人工智慧模型""",
        """聯合國《秘書長數位合作路線圖》提出的五大數位公共財包含：

- 開放資料
- 開源軟體
- 開放內容
- 開放標準
- 開放人工智慧模型""",
    )
    text = replace_block(
        text,
        """寬鬆
著作權規範強度
嚴謹
任何人修改、整合、合併使用此授權條款檔案的程式碼，都必須使用相同授權條款開源。
規定延伸至使用該授權條款檔案程式碼的網路服務，也必須公開完整的原始碼。
放寬僅透過函式庫介面使用此授權條款的檔案程式碼，無需開源。""",
        """GPL 家族可依著佐權義務強度整理如下：

| 授權條款 | 著佐權強度 | 核心義務 |
| --- | --- | --- |
| AGPL | 最嚴謹 | 使用 AGPL 授權檔案程式碼提供網路服務時，也必須公開完整原始碼。 |
| GPL | 嚴謹 | 修改、整合或合併 GPL 授權檔案程式碼時，須以相同授權條款開源。 |
| LGPL | 較寬鬆 | 僅透過函式庫介面使用 LGPL 授權檔案程式碼時，通常無需將整體專案開源。 |""",
    )
    text = replace_block(
        text,
        """嚴謹
著作權規範強度
寬鬆
任何人修改、整合、合併使用此授權條款類別檔案的程式碼，都必須使用相同授權條款開源。
又細分為 AGPL、GPL 和 LGPL 等。
只要有修改使用該授權條款的檔案，就必須公開該檔案的原始碼。
要求必須保留著作權與授權聲明，另參與之貢獻者皆應明確授予專利權。
僅需於散布原始碼時保留著作權與授權聲明。
僅需於散布原始碼時保留著作權與授權聲明。（散布編譯過的二進位檔時則不強制）
放棄著作權。""",
        """上述六種授權條款可由嚴謹到寬鬆整理如下：

| 授權類型 | 核心要求 |
| --- | --- |
| AGPL／GPL／LGPL | GPL 家族在觸發著佐權條件時，要求以相同授權條款釋出對應原始碼。 |
| MPL v2 | 只要修改 MPL 授權檔案，就必須公開該檔案的原始碼。 |
| Apache License v2 | 必須保留著作權與授權聲明，且貢獻者明確授予專利權。 |
| MIT License | 散布原始碼時須保留著作權與授權聲明。 |
| Boost Software License 1.0 | 散布原始碼時須保留著作權與授權聲明，散布編譯後二進位檔時則不強制。 |
| The Unlicense | 放棄著作權，將作品釋放至公共領域。 |""",
    )
    text = replace_block(
        text,
        """專有軟體及開源軟體主要差異說明
專有軟體
開源軟體
財務成本
| 軟體及服務
成本 | 軟體授權費 技術服務費 | 以技術服務費用為主 |
| --- | --- | --- |
安全管理
| 程式碼透明度 | 程式碼不公開，
由廠商維護 | 程式碼通常完全公開，
可由社群及大眾共同檢視 |
| --- | --- | --- |
| 漏洞修補機制 | 由廠商排程進行安全檢測並排程進行漏洞修補 | 社群監督強、更新頻繁，機關須關注社群動態並建立維護流程 |
導入方法
| 供應商合作 | 與單一廠商合作，通常為原廠或授權代理商 | 專案中可與一至多家廠商合作，選商限制較少 |
| --- | --- | --- |
| 系統整合 | 系統整合與客製化取決於產品提供之API或協定 | 通常使用開放標準，具較大的系統整合彈性 |
授權管理
| 授權模式 | 專屬授權，限制使用範圍 | 開放授權，允許修改與再散布 |
| --- | --- | --- |
| 使用限制 | 受著作權法保障，授權契約明確規範使用限制，通常禁止逆向工程 | 單一系統可能涉及多種授權條款之管理，並需檢查不同開源授權間的相容性 |""",
        """專有軟體及開源軟體主要差異如下：

| 面向 | 評估項目 | 專有軟體 | 開源軟體 |
| --- | --- | --- | --- |
| 財務成本 | 軟體及服務成本 | 軟體授權費與技術服務費。 | 以技術服務費用為主。 |
| 安全管理 | 程式碼透明度 | 程式碼不公開，由廠商維護。 | 程式碼通常完全公開，可由社群及大眾共同檢視。 |
| 安全管理 | 漏洞修補機制 | 由廠商排程進行安全檢測與漏洞修補。 | 社群監督強、更新頻繁，機關須關注社群動態並建立維護流程。 |
| 導入方法 | 供應商合作 | 與單一廠商合作，通常為原廠或授權代理商。 | 專案中可與一至多家廠商合作，選商限制較少。 |
| 導入方法 | 系統整合 | 系統整合與客製化取決於產品提供之 API 或協定。 | 通常使用開放標準，具較大的系統整合彈性。 |
| 授權管理 | 授權模式 | 專屬授權，限制使用範圍。 | 開放授權，允許修改與再散布。 |
| 授權管理 | 使用限制 | 受著作權法保障，授權契約明確規範使用限制，通常禁止逆向工程。 | 單一系統可能涉及多種授權條款之管理，並需檢查不同開源授權間的相容性。 |""",
    )
    text = replace_section(
        text,
        '<a id="2-2-1-open-source-software-benefits"></a>\n#### 2.2.1 開源軟體的使用效益\n\n',
        '\n<a id="2-2-2-risk-analysis-of-open-source-software"></a>',
        """公部門使用開源軟體進行資訊系統開發，除了是一項公開透明的數位治理實踐，在成本、安全性、客製化、系統整合力、合作廠商選擇以及政策價值等面向上也具備顯著效益。

| 效益 | 說明 |
| --- | --- |
| 政策與公共價值 | 公部門採開源不僅是技術選擇，更是政策宣示，強調數位工具服務公眾利益，提升系統透明度與可審查性，增進公民信任。 |
| 財務成本可預期性高 | 開源軟體免授權費，且未來維護費用機關具公平議價能力。 |
| 合作廠商選擇彈性高 | 開源軟體導入無須指定廠商，單位可自由選擇在地或國際廠商合作，降低供應商鎖定風險。 |
| 安全管理自主性高 | 公開原始碼有助公部門掌握系統、強化資安，社群與第三方也可及早發現並修補漏洞。 |
| 高度系統整合力 | 開源軟體多採標準協定與格式，易整合既有系統，並支援跨平臺協作。 |
| 高度客製化能力 | 開源軟體可自由修改，公部門可依業務流程調整功能、擴充模組與優化介面。 |
""",
    )
    text = replace_section(
        text,
        '<a id="2-2-2-risk-analysis-of-open-source-software"></a>\n#### 2.2.2 使用開源軟體風險評估\n\n',
        '\n<a id="2-3-open-source-software-implementation-model"></a>',
        """即使開源軟體的應用具備顯著效益，在資訊系統導入時仍須針對選型項目進行完整風險評估。風險評估流程可以與機關既有風險管理活動整合，包含：（1）蒐集目前及預計採用的開源軟體可能涉及的風險議題；（2）依據風險議題的發生機率與影響進行風險評分；（3）針對評分結果超過可接受風險值之風險議題，擬定因應方式。

常見風險如下：

| 風險 | 說明 |
| --- | --- |
| 轉型風險 | 從既有專有軟體轉換到開源軟體時，仍可能需投入大量人力與時間，包括資料遷移、流程再設計、系統驗證與員工訓練。 |
| 合作廠商品質與維護責任 | 開源專案雖有社群支援，但公共行政具備高度責任導向特性，仍須確保可靠的開發與維護團隊，並明確維護責任。 |
| 資安風險 | 使用開源軟體需搭配資安監控機制，以即時識別與修補軟體漏洞。 |
| 授權與法律風險 | 開源授權條款具有法律效力，若未妥善處理授權相容性，可能導致侵權風險。 |
| 使用者接受度 | 使用者可能已習慣 Microsoft Office 或 Google Workspace 等專有工具，需透過教育訓練與文化轉變提高採用意願。 |
""",
    )
    text = replace_section(
        text,
        '<a id="2-3-1-development-strategy-adopt-integrate-or-self-build"></a>\n#### 2.3.1 開發策略選擇：應用、整合或自主開發？\n\n',
        '\n<a id="2-3-2-explore-projects-and-referenceable-platform"></a>',
        """公部門使用開源軟體進行資訊系統開發時，應依專案需求、內部能力與長期治理需求選擇導入策略。

1. 應用（Adopt）：當專案需求已能明確對應至成熟開源專案軟體時，直接採用既有方案是具效率且風險較低的做法。其優勢包含節省建置時間、減少重複開發、共享全球社群經驗與安全更新、採用開放規格與標準，以及降低維運挑戰。

2. 整合式導入（Integrate）：透過組合多個開源專案（如框架、函式庫、資料平臺）形成具彈性且符合在地需求的解決方案。德國 openDesk 即是整合多項既有開源服務，打造符合公務機關需求的主權辦公套裝軟體。

3. 自主開發（Self-built）：在特殊需求或關鍵應用（Critical or Sovereign Systems）情境下，若既有開源專案無法滿足國內法規、行政流程、文化語言需求、國家安全或數位主權要求，應考量以自主開發為核心。

無論選擇哪一種策略，開源導入的成功關鍵在於「開放優先」（Open First）。專案初期即應預設未來可開源，並在系統架構、授權管理、文件撰寫上做好準備；只有在安全、隱私或尚未公開政策等必要理由下，才保留封閉部分。分層設計細節可參考英國政府指引《程式碼何時應開放或封閉》（Security Considerations When Coding in the Open）[^23]，其提醒：「安全應該設計在開放中，而不是封閉中」。

![開放優先安全治理示意圖](assets/zh-tw-image22.png)
""",
    )
    text = replace_block(
        text,
        """| 平臺 | 營運單位 | 資料庫特色 | 代表性專案 |
| --- | --- | --- | --- |
| Software 目錄
openCode.de | 德國 ZenDiS
（Zentrum für Digitale Souveränität，數位主權中心）| 聚焦數位主權與歐盟的法遵性，強調重用與可持續維護。 | openDesk
（詳如本手冊 1.[2.1](#2-1-difference-between-using-open-source-and-proprietary-software)）FIM（Federated Information Management, 聯邦資訊管理框架）Smart Village App
（地方治理應用）|
| SILL 資料庫
code.gouv.fr | 法國 DINUM（Direction Interministérielle du Numérique，跨部會數位總署）| 整合各部會已經採用並維運的自由軟體。 | OpenFisca
（社會政策模擬工具）GeoNature
（生態觀測與地理資訊系統）|
| DGPs 登錄庫
Digital Public Goods Registry | 聯合國數位公共財聯盟（Digital Public Goods Alliance, DPGA）由 UNICEF、UNDP、Norad 共同維運 | 聚焦得以促進 SDGs 永續發展目標開源軟體，每個專案均有通過開源、倫理、治理與透明性審查。 | DHIS2
（挪威：公共衛生資訊平臺）OpenCRVS
（民事登記系統）Wikipedia
（開放內容平臺）|
| 公共程式平臺 Code.gov.tw | 我國 數位發展部（Ministry of Digital Affairs, MoDA）| 我國政府逐步建立公共程式釋出平臺，整合開源專案與 API，推動跨部門協作與開放治理。 | 數位憑證皮夾 地址標準寫法 API 臺北程式設計節活動網站 |""",
        """| 平臺 | 營運單位 | 資料庫特色 | 代表性專案 |
| --- | --- | --- | --- |
| Software 目錄 openCode.de | 德國 ZenDiS（Zentrum für Digitale Souveränität，數位主權中心） | 聚焦數位主權與歐盟法遵性，強調重用與可持續維護。 | openDesk、FIM（Federated Information Management）、Smart Village App。 |
| SILL 資料庫 code.gouv.fr | 法國 DINUM（Direction Interministérielle du Numérique，跨部會數位總署） | 整合各部會已採用並維運的自由軟體。 | OpenFisca、GeoNature。 |
| Digital Public Goods Registry | 聯合國數位公共財聯盟（Digital Public Goods Alliance, DPGA），由 UNICEF、UNDP、Norad 共同維運 | 聚焦得以促進 SDGs 永續發展目標的開源軟體，每個專案均通過開源、倫理、治理與透明性審查。 | DHIS2、OpenCRVS、Wikipedia。 |
| 公共程式平臺 Code.gov.tw | 我國數位發展部（Ministry of Digital Affairs, MoDA） | 我國政府逐步建立公共程式釋出平臺，整合開源專案與 API，推動跨部門協作與開放治理。 | 數位憑證皮夾、地址標準寫法 API、臺北程式設計節活動網站。 |""",
    )
    text = replace_block(
        text,
        """供應鏈盲點
版本與維運風險
授權風險
廠商未揭露所有使用的開源套件，使機關無法掌握軟體物料清單，一旦上游開源元件出現漏洞，下游無法及時應變
不同系統使用同一開源元件的不同版本，造成機關內持長久維運困難與潛在衝突
開源授權繁多（例如 GPL、Apache、MIT），若未遵循義務，可能導致法律糾紛或被迫公開整個系統""",
        """| 風險 | 說明 |
| --- | --- |
| 供應鏈盲點 | 廠商若未揭露所有使用的開源套件，機關便無法掌握完整軟體物料清單；一旦上游開源元件出現漏洞，下游將難以及時應變。 |
| 版本與維運風險 | 不同系統使用同一開源元件的不同版本，可能造成長期維運困難與潛在衝突。 |
| 授權風險 | 開源授權繁多，例如 GPL、Apache、MIT；若未遵循義務，可能導致法律糾紛或被迫公開整個系統。 |""",
    )
    text = text.replace("\nImplementation of Open-Source Software\n\n<a id=\"chapter-3-open-source-software-implementation\"></a>", "\n<a id=\"chapter-3-open-source-software-implementation\"></a>")
    text = text.replace("\nMaintenance and Operation of\nOpen-Source Software\n\n<a id=\"chapter-4-open-source-software-maintenance-and-operations\"></a>", "\n<a id=\"chapter-4-open-source-software-maintenance-and-operations\"></a>")
    text = re.sub(r"(\[\^\d+\])(?=[\u4e00-\u9fff])", r"\1 ", text)
    text = re.sub(r"([\u4e00-\u9fff])(\[\^\d+\])", r"\1\2", text)
    path.write_text(text, encoding="utf-8")


def main() -> None:
    fix_en()
    fix_zh()


if __name__ == "__main__":
    main()
