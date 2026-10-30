# Assignment 2024-25 (Break-Even and Risk Analyses) Answering Booklet

Privacy-safe text transcript. Formatting, embedded figures and equations may differ from the original Office document.

 UESTC3031 - Engineering Project Management & Finance (2024 – 2025 Semester 2)

Break-Even and Risk Analysies (Assessment (Report))

The numbers in square brackets in the right-hand margin indicate the marks allotted to the part of the question against which the mark is shown. These marks are for guidance only.

Purpose of the Assignment

To demonstrate basics of engineering economics and break-even analysis / make-or- buy analysis

Date Issued to Students: 05th May 2025 / Monday Deadline / Submission Date: 15th May 2025 / Thursday Submission: via Moodle

Submission Instructions:

You must submit in ONE pdf document (not a zipped file, not two times, not in a word document) the break-even analysis report that accompanies it. You already have the instructions in the lecture notes and have been provided the assignment answering file that must be used.

You must prepare this assessment in pairs/groups of 2. You must clearly indicate in the file name and in the document the student name’s and IDs in the form Student1_GUID_UESTCID_Student2_GUID_UESTCID.pdf and inside the documents you will list a table with the student’s names, GUIDs, and UESTCIDs of your group members so that we know who submitted with whom.

You must submit a plagiarism declaration and your submission will go through

plagiarism check.

No late submissions will be allowed in the Moodle so if you don't submit you will get a zero for this complete assessment.

This is a SUMMATIVE assessment (i.e. marked assessment).

Only one student must submit the assessment prepared in groups so we must receive (via Moodle) only 1 submission in the system i.e. one for each group.

While using references, you must use IEEE style/format.

Imran Shafique Ansari

Break-Even and Risk Analyses Report[100 Marks]

Ⅰ. Calculation [45]

You are a production engineer in an electronics company responsible for making electronic circuit boards. A customer has come to you with a design for a microcontroller and has requested you a quote for their business. Your manager has provided you with the documentation from the customer that includes a Bill of Materials (BOM) (as given in the Appendix). He has also provided you with a list of components (see Table I) required for producing the product and their costs from your approved suppliers (as given in the Appendix).

Your manager has requested that you provide a detailed cost analysis for a few different production volumes. Examine your analysis based on the following:

Pablo is one of the employees in your company, if he borrowed £5000 from a bank at 5% interest, three end-of-year payments will be made.

a. At the end of the first year, he will repay half of the £5000 principal plus the interest that is due.

b. At the end of the second year, he will repay half of the remaining £2,500 principal plus interest due.

c. At the end of the third year, he will repay the final £1,250 principal plus interest due.

Please write the relevant formula and calculate the amount he should repay each year and draw the corresponding Cash Flow Diagram.[10/100]

Formula:

Annual Payment = Principal Repayment + Interest (5%) [1, Slide 23]

Let

P0=£5 000 be the initial principal,

r=5%=0.05 be the annual interest rate,

f=50%=0.5 be the fraction of principal repaid in each of the first two years.

1. General Recurrence for Years 1–2

At the start of year k (for k=1,2), the remaining principal is Pk−1

Payment in year kkk consists of:

Principal repaid: f Pk−1​

Interest due: r Pk−1

So the total payment in year k is

Ak=f Pk-1+r Pk-1=f+r Pk-1, k=1,2

After that payment, the remaining principal at end of year k becomes

Pk=Pk-1-f Pk-1=1-f Pk-1，k=1,2

2. Final (Year 3) Repayment

By the start of year 3, the remaining principal is P2​. In the third year the borrower repays all of P2 plus interest on it, so

A3=P2+r P2=1+r P2

Calculation

Year 1:

A1=f+r P0=0.5+0.05×5000=0.55×5000=£2750

P1=1-f P0=0.5×5000=£2500.

Year 2:

A2=f+r P1=0.55×2500=£1375,

P2=1-f P1=0.5×2500=£1250.

Year 3:

A3=1+r P2=1.05×1250=£1312.50.

So the three payments are

A1=£2 750  A2=£1375   A3=£1312.50

Corresponding Cash Flow Diagram

2. When producing a large number of PCBs (usually over 500), it takes a significant amount of time. To meet delivery deadlines, expedited shipping of raw materials is required to produce more than 500 PCBs.

Company A: The expedited shipping cost for raw materials per PCB is £1.5, with no additional charge.

Company B: The expedited shipping cost for raw materials per PCB is £1.3, but an additional £500 container rental fee is required.

Using the component cost figures provided, calculate the total cost to manufacture the following quantities of PCBs: 100, 1000, and 5000. Select the lowest cost method for each production quantity. Your answer must contain sufficient details for your work/calculations to be checked by your manager.

     [15/100]

Component

100 (£)

1 000 (£)

5 000 (£)

ATMega328 MCU

1.650

1.090

1.090

CH340G USB–UART

0.343

0.320

0.320

LM1117-3.3 V Regulator

0.605

0.364

0.349

LM1117-5.0 V Regulator

0.605

0.364

0.349

16 MHz Crystal

0.269

0.197

0.192

12 MHz Crystal

0.269

0.197

0.192

LED (Power)

0.052

0.039

0.039

LED (Pin 13)

0.052

0.039

0.039

47 µF Electrolytic ×2

0.298

0.188

0.146

100 nF Ceramic ×4

0.052

0.036

0.028

10 kΩ Resistor ×6

0.042

0.018

0.012

Reset Switch

0.193

0.132

0.124

DC Power Jack

0.877

0.835

0.835

USB Socket

0.324

0.203

0.166

Single-inline Conn. ×2

1.016

0.716

1.244¹

Dual-in-line Header

0.415

0.303

0.209

Total BOM cost/board

8.078

5.757

5.334

a. Per‐board BOM Cost (£/board)

b.Per‐board Fabrication & Assembly Costs (£/board)

Quantity

PCB Fab

Assembly

100

0.6904

3.7823

1 000

0.44397

0.78538

5 000

0.36110

0.47481

c. Shipping Cost

Company A: £1.50/board

Company B: £1.30/board + £500 one-time fee

d. Total Cost Formulas

For run size Q:

TotalAQ=CBOM+Cfab+Cassy Q+1.50 Q,

TotalBQ=CBOM+Cfab+Cassy Q+1.30 Q+500.

e. Numeric Results & Selection

QQ

∑cost/board

Total A (£)

Total B (£)

Cheaper

100

8.078+0.6904+3.7823 = 12.5507

12.5507×100+150 = 1 405.07

12.5507×100+130+500 = 1 885.07

A

1 000

5.757+0.44397+0.78538 = 6.98635

6.98635×1000+1500 = 8 486.35

6.98635×1000+1300+500 = 8 786.35

A

5 000

5.334+0.36110+0.47481 = 6.16991

6.16991×5000+7500 = 38 849.55

6.16991×5000+6500+500 = 37 849.55

B

Q=100 & 1 000: Company A is cheapest (no fixed fee dilution).

Q=5 000: Company B wins, as its lower per-board rate outweighs the £500 fee.

Thus, select Company A for runs up to 1 000 boards, and Company B for 5 000.

You have agreed a deal with your component suppliers, PCB manufacturers, and assembly operation on a total variable cost of £7.50 per board for all volumes between 0 and 5,000 boards. If your company has Fixed Costs of £19,500 and a selling price of £15.00, what is the Margin of Safety if you produce 4,000 boards? And what is the company profit when you produce 4000 boards? Draw a graph to illustrate this point.[12/100]

a. Definitions

Fixed Cost (FC): £19 500

Variable Cost per board (VC): £7.50

Selling Price per board (SP): £15.00

Production Level (Q): 4 000 boards

b. Break-Even Point (BEP)

The break-even point is the volume at which total revenue equals total cost (no profit, no loss). It is given by:

BEP=FCSP-VC=19 50015.00-7.50= 2 600.

(Formula from Lecture 11) .

c. Margin of Safety (MOS)

Margin of safety measures how far actual sales exceed the break-even volume, as a percentage of actual sales:

MOS=Q-BEPQ×100%=4 000-2 6004 000×100%= 35%.

(Definition from Lecture 11) .

d. Profit at 4 000 Units

Profit can be computed as

Profit=SP-VC×Q - FC=15.00-7.50×4 000-19 500= 7.50×4 000 - 19 500= 30 000 - 19 500= ￡10 500.

Your sales manager advises you that a new customer is willing to pay £27.00 per board but only for a maximum order of 1600 boards. How much profit or loss could you make on this order? Will there be a Margin of Safety in this case? If yes, calculate it. A graph is recommended.[8/100]

a. Known Data

Fixed Cost (FC): £19 500

Variable Cost per board (VC): £7.50

Special Order Price (SP′): £27.00 per board

Order Quantity (Q′): 1 600 boards

b. Profit Calculation

Use the standard profit formula:

Profit=SP'-VC×Q'-FC

Substitute in the numbers:

Profit=27.00-7.50×1600-19500= 19.50×1600 - 19500= 31200 - 1950= £11 700.

So the special order yields a profit of £11 700.

c. New Break-Even Point (BEP′)

Recompute BEP for the higher price:

BEP'=FCSP'-VC=1950027.00-7.50=1950019.50=1000 boards

d. Margin of Safety (MOS′)

Since Q′ exceeds BEP′, there is a safety margin:This means that even if sales dropped by 37.5%, the company would still break even.

MOS'=Q'-BEP'Q'×100\%=1600-10001600×100\%= 37.5\%.

Ⅱ. Extensive Discussion [55]

5. Risk Management

Provide 8 possible risks involved in the undertaken project in the form of Risk Register and perform quantitative analysis for schedule and cost impacts of listed risks in the form of influence diagrams learned in the class, respectively.  [15/100]

The following questions are based on the same background, for each (sub) question, the length must be no longer than 250 words.

6. Suppose you are the owner of Innovation Solution Inc., a start-up that has become highly successful by designing and selling specialized high-performance network routers (Product Line A) primarily to large enterprise data centers, the company is now planning to diversify its product range to create new profit points. The new product lines include Product Line B: Consumer-grade smart home hubs, which require faster development cycles, different marketing channels, and lower-cost manufacturing; and Product Line C: Custom IoT sensor arrays for specific industrial clients, which require close collaboration between specialized engineers, sales acting as consultants, and flexible operations for bespoke builds. How should the organizational structure of the company be adjusted to accommodate these new product lines and projects?[10/100]

For the custom IoT sensor arrays (Product Line C), what factors should Innovation Solution Inc. consider when deciding whether to make the sensors in-house or buy them from an external supplier? How would the company evaluate the need for control over the manufacturing process, quality, proprietary information, and the relationship with potential partners?[10/100]

Innovation Solution Inc. has diversified its product portfolio by adding consumer-grade smart home hubs (Product Line B) and custom IoT sensor arrays (Product Line C) to an already successful enterprise router business (Product Line A). Looking ahead:[10/100]

(a) Identify and Analyze New Market Opportunities:

How should the company identify and evaluate emerging market trends, technologies, or customer segments to further expand its business? Consider the role of market research, competitive analysis, and customer feedback in determining the direction for future expansion.

(b) Role of Strategic Partnerships and Acquisitions:

Discuss how forming strategic partnerships, joint ventures, or pursuing mergers and acquisitions could facilitate rapid entry into new markets or product areas. What criteria should be used to select the right partners or targets, and how can these move support both short-term profitability and long-term innovation?

(c) Balancing Innovation with Scalability:

As Innovation Solution Inc. grows its product mix, what measures should be in place to ensure that increased diversification does not dilute its core competencies and innovation capabilities? How might investments in R&D or technology platforms contribute to a sustainable competitive advantage?

Given the current operational shifts—serving a mix of high-performance enterprise products, consumer electronics, and custom industrial IoT solutions—Innovation Solution Inc. will face challenges in balancing efficiency, flexibility, and control as it grows. Consider the following:[10/100]

(a) Decentralization vs. Centralization:

Analyze the trade-offs between a centralized organizational structure and a decentralized (or matrix) organization for managing diverse product lines. How might each structure impact communication, decision-making, and responsiveness to market dynamics across the different business units?

(b) Scalable Organizational Design:

What organizational changes (such as establishing product-specific units, cross-functional teams, or dedicated innovation hubs) can support scalable growth as the company continues to expand? Evaluate the benefits and risks associated with each model in terms of maintaining quality, operational control, and proprietary advantages.

(c) Integration of Engineering and Finance Considerations:

In your answer, highlight how financial planning, budgeting, and performance metrics can be integrated within the organizational structure to align with strategic objectives. How can the company ensure that engineering innovations are efficiently transitioned to scalable production and market success without losing operational efficiency?

APPENDIX:Arduino UNO R3 BOM Costs

BOM Prices for 2025 (All prices in UKP)

LM1117 (5.0V or 3.3V)

Quantity

Price (each)

1+

0.916

50+

0.795

100+

0.605

250+

0.565

500+

0.525

1000+

0.364

2500+

0.356

5000+

0.349

Crystal (16MHz or 12MHz)

Quantity

Price (Each)

1+

0.444

50+

0.327

100 +

0.269

250 +

0.260

500 +

0.251

1000 +

0.197

5000 +

0.192

ATMega 328 Microcontroller

Quantity

Price(each)

1+

2.35

10+

2.06

25+

1.85

50+

1.72

100+

1.65

250+

1.49

500+

1.30

1000+

1.09

CH340G USB – Serial Interface

Quantity

Price(each)

1+

0.507

10+

0.391

30+

0.367

100+

0.343

500+

0.332

1000+

0.320

USB Socket

Quantity

Price(each)

5+

0.464

75+

0.324

150+

0.273

250+

0.216

500+

0.203

1500+

0.190

2500+

0.178

5000+

0.166

DC Power Socket

Quantity

Price(each)

1+

1.441

10+

1.069

25+

0.983

100+

0.877

250+

0.856

500+

0.835

47uF / 25V Electrolytic SMD

Quantity

Price(each)

10+

0.219

100+

0.149

500+

0.094

2500+

0.086

5000+

0.073

10000+

0.070

50000+

0.063

100nF / 10V ceramic 0603 SMD

Quantity

Price(each)

10+

0.024

100+

0.013

500+

0.011

1000+

0.009

2000+

0.008

4000+

0.007

20000+

0.006

10K Resistor / 0603 SMD.

Quantity

Price(each)

10+

0.010

100+

0.007

500+

0.004

1000+

0.003

2500+

0.002

LED SMD RED

Quantity

Price(each)

5+

0.102

25+

0.054

100+

0.052

250+

0.045

500+

0.040

1000+

0.039

Single In Line connector (8 way) [Assume same cost for 6 way and 10way]

Quantity

Price(each)

1+

0.722

10+

0.669

100+

0.508

500+

0.437

1000+

0.358

5000+

0.311

10000+

0.307

6-Way, Dual In-Line header, Through Hole

Quantity

Price (each)

1+

0.480

10+

0.450

50+

0.415

500+

0.303

1500+

0.260

2500+

0.209

SMD Switch (Reset)

Quantity

Price

10+

0.193

500+

0.166

1000+

0.132

5000+

0.124

10000+

0.119

PCB Cost: 2 layer, 53 x 68mm. (SEEED)

Qty

Price(UKP)

5

6.15

10

9.40

50

44.38

100

69.04

500

247.70

1000

443.97

2500

990.05

5000

1805.48

Assembly costs: 28 components; 7 thru’ hole, 18 SMT (PCBWAY)

Qty

Price (UKP) (for the given

quantity)

10

266.40

50

312.40

100

378.23

500

625.32

1000

785.38

2500

1600.02

5000

2374.05

Table I: List of Components, and their Quantities

Component

Description

Quantity

ATMega328

Microcontroller IC

1

CH340G

USB to Serial IC

1

LM1117-3.3

Linear Regulator IC (3.3V)

1

LM1117-5.0

Linear Regulator IC (5.0V)

1

Crystal, 12MHz- HC49 Package

USB Crystal

1

Crystal, 16MHz-HC49 Package

CPU Crystal

1

LED1 Red, SMT

LED, Power indication

1

LED2, Red, SMT

LED Indicator, Pin 13

1

C1, C2

Capacitor, electrolytic, 47uF, 25V

2

C3, C4, C5, C6

Capacitor, decoupling, 100nF, 10V, 0603

4

R1, R2, R3, R4, R7, R8

Resistor, 10K, 0603

6

SWT_1

Switch, NO, reset, SMT

1

CONN_1

DC Power Connector, Through hole

1

CONN_2

USB Connector, Through hole

1

SIP_1

8-Way Single In-Line Connector, Through

Hole

2

SIP_2

6-Way, Single In-Line Connector, Through

Hole

1

SIP_3

10-Way, Single In-Line Connector, Through

Hole

1

SIP_4

6-Way, Dual In-Line header, Through Hole

1

PCB_1

Printed Circuit Board, FR-4, Double sided,

1.6mm (53mm x 68mm)

1

ASSY_1

Board Assembly costs; 28 Component, 7 Through Hole

1

------------------------------------END OF ASSESSMENT ------------------------------------