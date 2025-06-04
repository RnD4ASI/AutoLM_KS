# Basel Committee on Banking Supervision 

## CRE

## Calculation of RWA for credit risk

## CRE32

IRB approach: risk components

## Version effective as of 01 Jan 2023

Changes due to the December 2017 Basel III publication and the revised implementation date announced on 27 March 2020.

This document has been generated on 10/04/2024 based on the Basel Framework data available on the BIS website (www.bis.org).

(c) Bank for International Settlements 2024. All rights reserved.

## Introduction

32.1 This chapter presents the calculation of the risk components (PD, LGD, EAD, M) that are used in the formulas set out in CRE31. In calculating these components, the legal certainty standards for recognising credit risk mitigation under the standardised approach to credit risk (CRE22) apply for both the foundation and advanced internal ratings-based (IRB) approaches.

## Risk components for corporate, sovereign and bank exposures

32.2 This section, CRE32.2 to CRE32.56, sets out the calculation of the risk components for corporate, sovereign and bank exposures. In the case of an exposure that is guaranteed by a sovereign, the floors that apply to the risk components do not apply to that part of the exposure covered by the sovereign guarantee (ie any part of the exposure that is not covered by the guarantee is subject to the relevant floors).

Probability of default (PD)

32.3 For corporate, sovereign and bank exposures, the PD is the one-year PD associated with the internal borrower grade to which that exposure is assigned. The PD of borrowers assigned to a default grade(s), consistent with the reference definition of default, is $100 \%$. The minimum requirements for the derivation of the PD estimates associated with each internal borrower grade are outlined in CRE36.77 to CRE36.79.

32.4 With the exception of exposures in the sovereign asset class, the PD for each exposure that is used as input into the risk weight formula and the calculation of expected loss must not be less than $0.05 \%$.

Loss given default (LGD)

32.5 A bank must provide an estimate of the LGD for each corporate, sovereign and bank exposure. There are two approaches for deriving this estimate: a foundation approach and an advanced approach. As noted in CRE30.34, the advanced approach is not permitted for exposures to certain entities.

LGD under the foundation internal ratings-based (F-IRB) approach: treatment of unsecured claims and non-recognised collateral

32.6 Under the foundation approach, senior claims on sovereigns, banks, securities firms and other financial institutions (including insurance companies and any financial institutions in the corporate asset class) that are not secured by recognised collateral will be assigned a $45 \%$ LGD. Senior claims on other corporates that are not secured by recognised collateral will be assigned a $40 \%$ LGD.

32.7 All subordinated claims on corporates, sovereigns and banks will be assigned a $75 \%$ LGD. A subordinated loan is a facility that is expressly subordinated to another facility. At national discretion, supervisors may choose to employ a wider definition of subordination. This might include economic subordination, such as cases where the facility is unsecured and the bulk of the borrower's assets are used to secure other exposures.

## LGD under the F-IRB approach: collateral recognition

32.8 In addition to the eligible financial collateral recognised in the standardised approach, under the F-IRB approach some other forms of collateral, known as eligible IRB collateral are also recognised. These include receivables, specified commercial and residential real
estate, and other physical collateral, where they meet the minimum requirements set out in CRE36.131 to CRE36.147. For eligible financial collateral, the requirements are identical to the operational standards as set out in the credit risk mitigation section of the standardised approach (see CRE22).

32.9 The simple approach to collateral presented in the standardised approach is not available to banks applying the IRB approach.

32.10 The LGD applicable to a collateralised transaction (LGD*) must be calculated as the exposure weighted average of the LGD applicable to the unsecured part of an exposure (LGD) and the LGD applicable to the collateralised part of an exposure (LGD). Specifically, the formula that follows must be used, where:

(1) E is the current value of the exposure (ie cash lent or securities lent or posted). In the case of securities lent or posted the exposure value has to be increased by applying the appropriate haircuts (HE) according to the comprehensive approach for financial collateral.

(2) ES is the current value of the collateral received after the application of the haircut applicable for the type of collateral $(\mathrm{Hc})$ and for any currency mismatches between the exposure and the collateral, as specified in CRE32.11 to CRE32.12. ES is capped at the value of $E \quad(1+\mathrm{HE})$.

(3) $\mathrm{EU}=\mathrm{E} \quad(1+\mathrm{HE})-\mathrm{Es}$. The terms $\mathrm{EU}$ and $\mathrm{ES}$ are only used to calculate LGD*. Banks must continue to calculate EAD without taking into account the presence of any collateral, unless otherwise specified.

(4) LGDU is the LGD applicable for an unsecured exposure, as set out in CRE32.6 and CRE32.7.

(5) LGDS is the LGD applicable to exposures secured by the type of collateral used in the transaction, as specified in CRE32.11.

$L G D^{*}=L G D_{U} \cdot \frac{E_{U}}{E \cdot\left(1+H_{E}\right)}+L G D_{S} \cdot \frac{E_{S}}{E \cdot\left(1+H_{E}\right)}$

32.11 The following table specifies the LGD and haircuts applicable in the formula set out in CRE32.10:

| Type of collateral | LGD $_{\mathrm{s}}$ | Haircut |
| :--- | :--- | :--- |
| Eligible financial collateral | $0 \%$ | As determined by the haircuts that apply in the comprehensive <br> formula of the standardised approach for credit risk (CRE22.49 <br> for jurisdictions that allow the use of ratings for regulatory <br> purposes and CRE22.50 for jurisdictions that do not). The <br> haircuts have to be adjusted for different holding periods and <br> non-daily remargining or revaluation according to CRE22.56 to <br> CRE22.59 of the standardised approach. |
| Eligible receivables | $20 \%$ | $40 \%$ |
| Eligible residential real estate / | $20 \%$ | $40 \%$ |
| commercial real estate | $25 \%$ | $40 \%$ |
| Other eligible physical collateral | Not applicable | $100 \%$ |

32.12 When eligible collateral is denominated in a different currency to that of the exposure, the haircut for currency risk is the same haircut that applies in the comprehensive approach

(CRE22.52 of the standardised approach).

32.13 Banks that lend securities or post collateral must calculate capital requirements for both of the following: (i) the credit risk or market risk of the securities, if this remains with the bank; and (ii) the counterparty credit risk arising from the risk that the borrower of the securities may default. CRE32.37 to CRE32.43 set out the calculation the EAD arising from transactions that give rise to counterparty credit risk. For such transactions the LGD of the counterparty must be determined using the LGD specified for unsecured exposures, as set out in CRE32.6 and CRE32.7.

LGD under the F-IRB approach: methodology for the treatment of pools of collateral

32.14 In the case where a bank has obtained multiple types of collateral it may apply the formula set out in CRE32.10 sequentially for each individual type of collateral. In doing so, after each step of recognising one individual type of collateral, the remaining value of the unsecured exposure (E) will be reduced by the adjusted value of the collateral (E) recognised in that step. In line with CRE32.10, the total of E across all collateral types is capped at the value of $E \quad(1+H)$. This results in the formula that follows, where for each collateral type i:

(1) LGDSi is the LGD applicable to that form of collateral (as specified in CRE32.11).

(2) ESi is the current value of the collateral received after the application of the haircut applicable for the type of collateral (Hc) (as specified in CRE32.11).

$L G D^{*}=L G D_{U} \cdot \frac{E_{U}}{E \cdot\left(1+H_{E}\right)}+\sum_{i} L G D_{S i} \cdot \frac{E_{S i}}{E \cdot\left(1+H_{E}\right)}$

## LGD under the advanced approach

32.15 Subject to certain additional minimum requirements specified below (and the conditions set out in CRE30.34), supervisors may permit banks to use their own internal estimates of LGD for corporate and sovereign exposures. LGD must be measured as the loss given default as a percentage of the EAD. Banks eligible for the IRB approach that are unable to meet these additional minimum requirements must utilise the foundation LGD treatment described above.

32.16 The LGD for each corporate exposure that is used as input into the risk weight formula and the calculation of expected loss must not be less than the parameter floors indicated in the table below (the floors do not apply to the LGD for exposures in the sovereign asset class):

| Unsecured | Secured |
| :---: | :---: |
| $25 \%$ | Varying by collateral type: <br> - $0 \%$ financial <br> - $10 \%$ receivables <br> - $10 \%$ commercial or residential real estate <br> - $15 \%$ other physical |

32.17 The LGD floors for secured exposures in the table above apply when the exposure is fully secured (ie the value of collateral after the application of haircuts exceeds the value of the exposure). The LGD floor for a partially secured exposure is calculated as a weighted average of the unsecured LGD floor for the unsecured portion and the secured LGD floor for the secured portion. That is, the following formula should be used to determine the LGD floor, where:

(1) LGDU floor and LGDS floor are the floor values for fully unsecured and fully secured exposures respectively, as specified in the table in CRE32.16.

(2) The other terms are defined as set out in CRE32.10 and CRE32.11.

Floor $=L G D_{U \text { filoor }} \cdot \frac{E_{U}}{E \cdot\left(1+H_{E}\right)}+L G D_{\text {sfloor }} \cdot \frac{E_{S}}{E \cdot\left(1+H_{E}\right)}$

32.18 In cases where a bank has met the conditions to use their own internal estimates of LGD for a pool of unsecured exposures, and takes collateral against one of these exposures, it may not be able to model the effects of the collateral (ie it may not have enough data to model the effect of the collateral on recoveries). In such cases, the bank is permitted to apply the formula set out in CRE32.10 or CRE32.14, with the exception that the LGD term would be the bank's own internal estimate of the unsecured LGD. To adopt this treatment the collateral must be eligible under the F-IRB and the bank's estimate of LGD must not take account of any effects of collateral recoveries.

32.19 The minimum requirements for the derivation of LGD estimates are outlined in CRE36.83 to CRE36.88.

## Treatment of certain repo-style transactions

32.20 Banks that want to recognise the effects of master netting agreements on repo-style transactions for capital purposes must apply the methodology outlined in CRE32.38 for determining $\mathrm{E}^{*}$ for use as the EAD in the calculation of counterparty credit risk. For banks using the advanced approach, own LGD estimates would be permitted for the unsecured equivalent amount ( $\mathrm{E}^{\star}$ ) used to calculate counterparty credit risk. In both cases banks, in addition to counterparty credit risk, must also calculate the capital requirements relating to any credit or market risk to which they remain exposed arising from the underlying securities in the master netting agreement.

## Treatment of guarantees and credit derivatives

32.21 There are two approaches for recognition of credit risk mitigation (CRM) in the form of guarantees and credit derivatives in the IRB approach: a foundation approach for banks using supervisory values of LGD, and an advanced approach for those banks using their own internal estimates of LGD.

32.22 Under either approach, CRM in the form of guarantees and credit derivatives must not reflect the effect of double default (see CRE36.102). As such, to the extent that the CRM is recognised by the bank, the adjusted risk weight will not be less than that of a comparable direct exposure to the protection provider. Consistent with the standardised approach, banks may choose not to recognise credit protection if doing so would result in a higher capital requirement.

32.23 For banks using the foundation approach for LGD, the approach to guarantees and credit derivatives closely follows the treatment under the standardised approach as specified in CRE22.70 to CRE22.84. The range of eligible guarantors is the same as under the standardised approach except that companies that are internally rated may also be recognised under the foundation approach. To receive recognition, the requirements outlined in CRE22.70 to CRE22.75 of the standardised approach must be met.

32.24 Eligible guarantees from eligible guarantors will be recognised as follows:

(1) For the covered portion of the exposure, a risk weight is derived by taking:

(a) the risk-weight function appropriate to the type of guarantor, and

(b) the PD appropriate to the guarantor's borrower grade.

(2) The bank may replace the LGD of the underlying transaction with the LGD applicable to the guarantee taking into account seniority and any collateralisation of a guaranteed commitment. For example, when a bank has a subordinated claim on the borrower but the guarantee represents a senior claim on the guarantor this may be reflected by using an LGD applicable for senior exposures (see CRE32.6) instead of an LGD applicable for subordinated exposures.

(3) In case the bank applies the standardised approach to direct exposures to the guarantor it may only recognise the guarantee by applying the standardised approach to the covered portion of the exposure.

32.25 The uncovered portion of the exposure is assigned the risk weight associated with the underlying obligor.

32.26 Where partial coverage exists, or where there is a currency mismatch between the underlying obligation and the credit protection, it is necessary to split the exposure into a covered and an uncovered amount. The treatment in the foundation approach follows that outlined in CRE22.80 to CRE22.81 of the standardised approach, and depends upon whether the cover is proportional or tranched.

Treatment of guarantees and credit derivatives: recognition under the advanced approach

32.27 Banks using the advanced approach for estimating LGDs may reflect the risk-mitigating effect of guarantees and credit derivatives through either adjusting PD or LGD estimates. Whether adjustments are done through PD or LGD, they must be done in a consistent manner for a given guarantee or credit derivative type. In doing so, banks must not include the effect of double default in such adjustments. Thus, the adjusted risk weight must not be less than that of a comparable direct exposure to the protection provider. In case the bank applies the standardised approach to direct exposures to the guarantor it may only recognise the guarantee by applying the standardised approach to the covered portion of the exposure. In case the bank applies the F-IRB approach to direct exposures to the guarantor it may only recognise the guarantee by determining the risk weight for the comparable direct exposure to the guarantor according to the F-IRB approach.

32.28 A bank relying on own-estimates of LGD has the option to adopt the treatment outlined in CRE32.23 to CRE32.26 above for banks under the F-IRB approach, or to make an adjustment to its LGD estimate of the exposure to reflect the presence of the guarantee or credit derivative. Under this option, there are no limits to the range of eligible guarantors although the set of minimum requirements provided in CRE36.104 to CRE36.105 concerning the type of guarantee must be satisfied. For credit derivatives, the
requirements of CRE36.110 to CRE36.111 must be satisfied. ${ }^{1}$ For exposures for which a bank has permission to use its own estimates of LGD, the bank may recognise the risk mitigating effects of first-to-default credit derivatives, but may not recognise the risk mitigating effects of second-to-default or more generally nth-to-default credit derivatives. Footnotes

1 When credit derivatives do not cover the restructuring of the underlying obligation, the partial recognition set out in CRE22.75 of the standardised approach applies.

## Exposure at default (EAD)

32.29 The following sections apply to both on and off-balance sheet positions. All exposures are measured gross of specific provisions or partial write-offs. The EAD on drawn amounts should not be less than the sum of: (i) the amount by which a bank's regulatory capital would be reduced if the exposure were written-off fully; and (ii) any specific provisions and partial write-offs. When the difference between the instrument's EAD and the sum of (i) and (ii) is positive, this amount is termed a discount. The calculation of risk-weighted assets is independent of any discounts. Under the limited circumstances described in CRE35.4, discounts may be included in the measurement of total eligible provisions for purposes of the EL-provision calculation set out in CRE35.

## Exposure measurement for on-balance sheet items

32.30 On-balance sheet netting of loans and deposits will be recognised subject to the same conditions as under CRE22.68 of the standardised approach. Where currency or maturity mismatched on-balance sheet netting exists, the treatment follows the standardised approach, as set out in CRE22.10 and CRE22.12 to CRE22.15.

Exposure measurement for off-balance sheet items (with the exception of derivatives)

32.31 For off-balance sheet items there are two approaches for the estimation of EAD: a foundation approach and an advanced approach. When only the drawn balances of revolving facilities have been securitised, banks must ensure that they continue to hold required capital against the undrawn balances associated with the securitised exposures.

32.32 In the foundation approach, EAD is calculated as the committed but undrawn amount multiplied by a credit conversion factor (CCF). In the advanced approach, EAD for undrawn commitments may be calculated as the committed but undrawn amount multiplied by a CCF or derived from direct estimates of total facility EAD. In both the foundation approach and advanced approaches, the definition of commitments is the same as in the standardised approach, as set out in CRE20.94.

## EAD under the foundation approach

32.33 The types of instruments and the CCFs applied to them under the F-IRB approach are the same as those in the standardised approach, as set out in CRE20.94 to CRE20.101.

32.34 The amount to which the CCF is applied is the lower of the value of the unused committed credit line, and the value that reflects any possible constraining of the availability of the facility, such as the existence of a ceiling on the potential lending amount which is related to a borrower's reported cash flow. If the facility is constrained in this way, the bank must have sufficient line monitoring and management procedures to support this contention.

32.35 Where a commitment is obtained on another off-balance sheet exposure, banks under the foundation approach are to apply the lower of the applicable CCFs.

32.36 Banks which meet the minimum requirements for use of their own estimates of EAD (see CRE36.89 to CRE36.98) will be allowed for exposures for which A-IRB is permitted (see CRE30.33) to use their own internal estimates of EAD for undrawn revolving commitments ${ }^{2}$ to extend credit, purchase assets or issue credit substitutes provided the exposure is not subject to a CCF of $100 \%$ in the foundation approach (see CRE32.33). Standardised approach CCFs must be used for all other off-balance sheet items (for example, undrawn non-revolving commitments), and must be used where the minimum requirements for own estimates of EAD are not met. The EAD for each exposure that is not in the sovereign asset class that is used as input into the risk weight formula and the calculation of expected loss is subject to a floor that is the sum of: (i) the on balance sheet amount; and (ii) $50 \%$ of the off balance sheet exposure using the applicable CCF in the standardised approach.

Footnotes

$2 \quad$ A revolving loan facility is one that lets a borrower obtain a loan where the borrower has the flexibility to decide how often to withdraw from the loan and at what time intervals. A revolving facility allows the borrower to drawdown, repay and re-draw loans advanced to it. Facilities that allow prepayments and subsequent redraws of those prepayments are considered as revolving.

## Exposures that give rise to counterparty credit risk

32.37 For exposures that give rise to counterparty credit risk according to CRE51.4 (ie OTC derivatives, exchange-traded derivatives, long settlement transactions and securities financing transactions (SFTs)), the EAD is to be calculated under the rules set forth in CRE50 to CRE54.

32.38 For SFTs, banks may recognise a reduction in the counterparty credit risk requirement arising from the effect of a master netting agreement providing that it satisfies the criteria set out in CRE22.62 and CRE22.63 of the standardised approach. The bank must calculate $\mathrm{E}^{*}$, which is the exposure to be used for the counterparty credit risk requirement taking account of the risk mitigation of collateral received, using the formula set out in CRE22.65 of the standardised approach. In calculating risk-weighted assets and expected loss (EL) amounts for the counterparty credit risk arising from the set of transactions covered by the master netting agreement, $\mathrm{E*}$ must be used as the EAD of the counterparty.

32.39 As an alternative to the use of standard haircuts for the calculation of the counterparty credit risk requirement for SFTs set out in CRE32.38, banks may be permitted to use a value-at-risk (VaR) models approach to reflect price volatility of the exposures and the financial collateral. This approach can take into account the correlation effects between security positions. This approach applies to single SFTs and SFTs covered by netting agreements on a counterparty-by-counterparty basis, both under the condition that the collateral is revalued on a daily basis. This holds for the underlying securities being different and unrelated to securitisations. The master netting agreement must satisfy the criteria set out in CRE22.62 and CRE22.63 of the standardised approach. The VaR models approach is available to banks that have received supervisory recognition for an internal market risk model according to MAR30.2. Banks which have not received market risk model recognition can separately apply for supervisory recognition to use their internal VaR models for the calculation of potential price volatility for SFTs, provided the model meets the requirements of MAR30.2. Although the market risk standards have changed from a $99 \%$ VaR to a $97.5 \%$ expected shortfall, the VaR models approach to SFTs retains
the use of a $99 \%$ VaR to calculate the counterparty credit risk for SFTs. The VaR model needs to capture risk sufficient to pass the backtesting and profit and loss attribution tests of MAR30.4. The default risk charge of MAR33.18 to MAR33.39 is not required in the VaR model for SFTs.

32.40 The quantitative and qualitative criteria for recognition of internal market risk models for SFTs are in principle the same as in MAR30.5 to MAR30.16 and MAR33.1 to MAR33.12. The minimum liquidity horizon or the holding period for SFTs is 5 business days for margined repo-style transactions, rather than the 10 business days in MAR33.12. For other transactions eligible for the VaR models approach, the 10 business day holding period will be retained. The minimum holding period should be adjusted upwards for market instruments where such a holding period would be inappropriate given the liquidity of the instrument concerned.

32.41 The calculation of the exposure $\mathrm{E}^{*}$ for banks using their internal model to calculate their counterparty credit risk requirement will be as follows, where banks will use the previous day's VaR number:

$E^{*}=\max \left\{0,\left[\left(\sum E-\sum C\right)+\right.\right.$ VaRoutput from internal model $\left.]\right\}$

32.42 Subject to supervisory approval, instead of using the VaR approach, banks may also calculate an effective expected positive exposure for repo-style and other similar SFTs, in accordance with the internal models method set out in the counterparty credit risk standards.

32.43 As in the standardised approach, for transactions where the conditions in CRE22.36 are met, and in addition, the counterparty is a core market participant as specified in CRE22.37, supervisors may choose not to apply the haircuts specified under the comprehensive approach, but instead to apply a zero H. A netting set that contains any transaction that does not meet the requirements in CRE22.36 of the standardised approach is not eligible for this treatment.

## Effective maturity (M)

32.44 Effective maturity (M) will be 2.5 years for exposures to which the bank applies the foundation approach, except for repo-style transactions where the effective maturity is 6 months (ie $\mathrm{M}=0.5$ ). National supervisors may choose to require all banks in their jurisdiction (those using the foundation and advanced approaches) to measure $\mathrm{M}$ for each facility using the definition provided below.

32.45 Banks using any element of the A-IRB approach are required to measure effective maturity for each facility as defined below. However, national supervisors may allow the effective maturity to be fixed at 2.5 years (the "fixed maturity treatment") for facilities to certain smaller domestic corporate borrowers if the reported sales (ie turnover) as well as total assets for the consolidated group of which the firm is a part of are less than $€ 500$ million. The consolidated group has to be a domestic company based in the country where the fixed maturity treatment is applied. If adopted, national supervisors must apply the fixed maturity treatment to all IRB banks using the advanced approach in that country, rather than on a bank-by-bank basis.

32.46 Except as noted in CRE32.51, the effective maturity (M) is subject to a floor of one year and a cap of 5 years.

32.47 For an instrument subject to a determined cash flow schedule, effective maturity $\mathrm{M}$ is defined as follows, where CF denotes the cash flows (principal, interest payments and fees) contractually payable by the borrower in period $\mathrm{t}$ :

Effective maturity $=\mathrm{M}=\sum_{t} t \cdot C F_{t} / \sum_{t} C F_{t}$

32.48 If a bank is not in a position to calculate the effective maturity of the contracted payments as noted above, it is allowed to use a more conservative measure of $M$ such as that it equals the maximum remaining time (in years) that the borrower is permitted to take to fully discharge its contractual obligation (principal, interest, and fees) under the terms of Ioan agreement. Normally, this will correspond to the nominal maturity of the instrument.

32.49 For derivatives subject to a master netting agreement, the effective maturity is defined as the weighted average maturity of the transactions within the netting agreement. Further, the notional amount of each transaction should be used for weighting the maturity.

32.50 For revolving exposures, effective maturity must be determined using the maximum contractual termination date of the facility. Banks must not use the repayment date of the current drawing.

32.51 The one-year floor, set out in CRE32.46 above, does not apply to certain short-term exposures, comprising fully or nearly-fully collateralised ${ }^{3}$ capital market-driven transactions (ie OTC derivatives transactions and margin lending) and repo-style transactions (ie repos/reverse repos and securities lending/borrowing) with an original maturity of less than one year, where the documentation contains daily remargining clauses. For all eligible transactions the documentation must require daily revaluation, and must include provisions that must allow for the prompt liquidation or setoff of the collateral in the event of default or failure to re-margin. The maturity of such transactions must be calculated as the greater of one-day, and the effective maturity ( $\mathrm{M}$, consistent with the definition above), except for transactions subject to a master netting agreement, where the floor is determined by the minimum holding period for the transaction type, as required by CRE32.54.

Footnotes

3 The intention is to include both parties of a transaction meeting these conditions where neither of the parties is systematically under-collateralised.

32.52 The one-year floor, set out in CRE32.46 above, also does not apply to the following exposures:

(1) Short-term self-liquidating trade transactions. Import and export letters of credit and similar transactions should be accounted for at their actual remaining maturity.

(2) Issued as well as confirmed letters of credit that are short term (ie have a maturity below one year) and self-liquidating.

32.53 In addition to the transactions considered in CRE32.51 above, other short-term exposures with an original maturity of less than one year that are not part of a bank's ongoing financing of an obligor may be eligible for exemption from the one-year floor. After a careful review of the particular circumstances in their jurisdictions, national supervisors should define the types of short-term exposures that might be considered eligible for this treatment. The results of these reviews might, for example, include transactions such as:

(1) Some capital market-driven transactions and repo-style transactions that might not fall within the scope of CRE32.51.

(2) Some trade finance transactions that are not exempted by CRE32.52.

(3) Some exposures arising from settling securities purchases and sales. This could also include overdrafts arising from failed securities settlements provided that such overdrafts do not continue more than a short, fixed number of business days.

(4) Some exposures arising from cash settlements by wire transfer, including overdrafts arising from failed transfers provided that such overdrafts do not continue more than a short, fixed number of business days.

(5) Some exposures to banks arising from foreign exchange settlements.

(6) Some short-term loans and deposits.

32.54 For transactions falling within the scope of CRE32.51 subject to a master netting agreement, the effective maturity is defined as the weighted average maturity of the transactions. A floor equal to the minimum holding period for the transaction type set out in CRE22.57 of the standardised approach will apply to the average. Where more than one transaction type is contained in the master netting agreement a floor equal to the highest holding period will apply to the average. Further, the notional amount of each transaction should be used for weighting maturity.

32.55 Where there is no explicit definition, the effective maturity (M) assigned to all exposures is set at 2.5 years unless otherwise specified in CRE32.44.

## Treatment of maturity mismatches

32.56 The treatment of maturity mismatches under IRB is identical to that in the standardised approach (see CRE22.10 to CRE22.14).

## Risk components for retail exposures

32.57 This section, CRE32.57 to CRE32.67, sets out the calculation of the risk components for retail exposures. In the case of an exposure that is guaranteed by a sovereign, the floors that apply to the risk components do not apply to that part of the exposure covered by the sovereign guarantee (ie any part of the exposure that is not covered by the guarantee is subject to the relevant floors).

Probability of default (PD) and loss given default (LGD)

32.58 For each identified pool of retail exposures, banks are expected to provide an estimate of the PD and LGD associated with the pool, subject to the minimum requirements as set out in CRE36. Additionally, the PD for retail exposures is the greater of: (i) the one-year PD associated with the internal borrower grade to which the pool of retail exposures is assigned; and (ii) $0.1 \%$ for qualifying revolving retail exposure (QRRE) revolvers (see CRE30.24 for the definition of QRRE revolvers) and $0.05 \%$ for all other exposures. The LGD for each exposure that is used as input into the risk weight formula and the calculation of expected loss must not be less than the parameter floors indicated in the table below:

| LGD parameter floors for retail exposures |  | Secured |
| :--- | :--- | :--- |
| Type of exposure | Unsecured | $5 \%$ |
| Mortgages | Not applicable | Not applicable |
| QRRE (transactors and revolvers) | $50 \%$ |  |
| Other retail | $30 \%$ | Varying by collateral type: |


|  |  |  |
| :--- | :--- | :--- |
|  |  |  |
|  |  | $0 \%$ financial |
|  |  | $10 \%$ receivables |
| - $10 \%$ commercial or residential real estate |  |  |
|  |  | $15 \%$ other physical |

32.59 Regarding the LGD parameter floors set out in the table above, the LGD floors for partially secured exposures in the "other retail" category should be calculated according to the formula set out in CRE32.17. The LGD floor for residential mortgages is fixed at $5 \%$, irrespective of the level of collateral provided by the property.

Recognition of guarantees and credit derivatives

32.60 Banks may reflect the risk-reducing effects of guarantees and credit derivatives, either in support of an individual obligation or a pool of exposures, through an adjustment of either the PD or LGD estimate, subject to the minimum requirements in CRE36.100 to CRE36.111. Whether adjustments are done through PD or LGD, they must be done in a consistent manner for a given guarantee or credit derivative type. In case the bank applies the standardised approach to direct exposures to the guarantor it may only recognise the guarantee by applying the standardised approach risk weight to the covered portion of the exposure.

32.61 Consistent with the requirements outlined above for corporate and bank exposures, banks must not include the effect of double default in such adjustments. The adjusted risk weight must not be less than that of a comparable direct exposure to the protection provider. Consistent with the standardised approach, banks may choose not to recognise credit protection if doing so would result in a higher capital requirement.

## Exposure at default (EAD)

32.62 Both on- and off-balance sheet retail exposures are measured gross of specific provisions or partial write-offs. The EAD on drawn amounts should not be less than the sum of: (i) the amount by which a bank's regulatory capital would be reduced if the exposure were written-off fully; and (ii) any specific provisions and partial write-offs. When the difference between the instrument's EAD and the sum of (i) and (ii) is positive, this amount is termed a discount. The calculation of risk-weighted assets is independent of any discounts. Under the limited circumstances described in CRE35.4, discounts may be included in the measurement of total eligible provisions for purposes of the EL-provision calculation set out in chapter CRE35.

32.63 On-balance sheet netting of loans and deposits of a bank to or from a retail customer will be permitted subject to the same conditions outlined in CRE22.68 and CRE22.69 of the standardised approach. The definition of commitment is the same as in the standardised approach, as set out in CRE20.94. Banks must use their own estimates of EAD for undrawn revolving commitments to extend credit, purchase assets or issue credit substitutes provided the exposure is not subject to a CCF of $100 \%$ in the standardised approach (see CRE20.92) and the minimum requirements in CRE36.89 to CRE36.99 are satisfied. Foundation approach CCFs must be used for all other off-balance sheet items (for example, undrawn non-revolving commitments), and must be used where the minimum requirements for own estimates of EAD are not met.

32.64 Regarding own estimates of EAD, the EAD for each exposure that is used as input into the risk weight formula and the calculation of expected loss is subject to a floor that is the sum of: (i) the on balance sheet amount; and (ii) $50 \%$ of the off balance sheet exposure using the applicable CCF in the standardised approach.

32.65 For retail exposures with uncertain future drawdown such as credit cards, banks must take into account their history and/or expectation of additional drawings prior to default in their overall calibration of loss estimates. In particular, where a bank does not reflect conversion factors for undrawn lines in its EAD estimates, it must reflect in its LGD estimates the likelihood of additional drawings prior to default. Conversely, if the bank does not incorporate the possibility of additional drawings in its LGD estimates, it must do so in its EAD estimates.

32.66 When only the drawn balances of revolving retail facilities have been securitised, banks must ensure that they continue to hold required capital against the undrawn balances associated with the securitised exposures using the IRB approach to credit risk for commitments.

32.67 To the extent that foreign exchange and interest rate commitments exist within a bank's retail portfolio for IRB purposes, banks are not permitted to provide their internal assessments of credit equivalent amounts. Instead, the rules for the standardised approach continue to apply.

