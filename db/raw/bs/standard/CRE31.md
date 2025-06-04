# Basel Committee on Banking Supervision 

## CRE

## Calculation of RWA for credit risk

## CRE31

![](https://cdn.mathpix.com/cropped/2024_06_17_a787f32ab8da47503aebg-1.jpg?height=580&width=580&top_left_y=1115&top_left_x=224)

IRB approach: risk weight functions

## Version effective as of 01 Jan 2023

Changes due to December 2017 Basel III publication and the revised implementation date announced on 27 March 2020.

This document has been generated on 10/04/2024 based on the Basel Framework data available on the BIS website (www.bis.org).

(c) Bank for International Settlements 2024. All rights reserved.

## Introduction

31.1 This chapter presents the calculation of risk weighted assets under the internal ratingsbased (IRB) approach for: (i) corporate, sovereign and bank exposures; and (ii) retail exposures. Risk weighted assets are designed to address unexpected losses from exposures. The method of calculating expected losses, and for determining the difference between that measure and provisions, is described CRE35.

## Explanation of the risk-weight functions

31.2 Regarding the risk-weight functions for deriving risk weighted assets set out in this chapter:

(1) Probability of default (PD) and loss-given-default (LGD) are measured as decimals

(2) Exposure at default (EAD) is measured as currency (eg euros), except where explicitly noted otherwise

(3) In denotes the natural logarithm

(4) $\mathrm{N}(\mathrm{x})$ denotes the cumulative distribution function for a standard normal random variable (ie the probability that a normal random variable with mean zero and variance of one is less than or equal to $x$ ). The normal cumulative distribution function is, for example, available in Excel as the function NORMSDIST.

(5) $G(z)$ denotes the inverse cumulative distribution function for a standard normal random variable (ie the value of $x$ such that $N(x)=z$ ). The inverse of the normal cumulative distribution function is, for example, available in Excel as the function NORMSINV.

## Risk-weighted assets for exposures that are in default

31.3 The capital requirement $(\mathrm{K})$ for a defaulted exposure is equal to the greater of zero and the difference between its LGD (described in CRE36.83) and the bank's best estimate of expected loss (described in CRE36.86). The risk-weighted asset amount for the defaulted exposure is the product of $\mathrm{K}, 12.5$, and the EAD.

## Risk-weighted assets for corporate, sovereign and bank exposures that are not in default

## Risk-weight functions for corporate, sovereign and bank exposures

31.4 The derivation of risk-weighted assets is dependent on estimates of the PD, LGD, EAD and, in some cases, effective maturity (M), for a given exposure.

31.5 For exposures not in default, the formula for calculating risk-weighted assets is as follows (illustrative risk weights are shown in CRE99):

Correlation $=R=0.12 \cdot \frac{\left(1-e^{-50 \cdot P D}\right)}{\left(1-e^{-50}\right)}+0.24 \cdot\left(1-\frac{\left(1-e^{-50 \cdot P D}\right)}{\left(1-e^{-50}\right)}\right)$

Maturity adjustment $=b=[0.11852-0.05478 \cdot \ln (P D)]^{2}$

Capital requirement $=K=\left[L G D \cdot N\left[\frac{G(P D)}{\sqrt{(1-R)}}+\sqrt{\frac{R}{1-R}} \cdot G(0.999)\right]-P D \cdot L G D\right] \cdot \frac{(1+(M-2.5) \cdot b)}{(1-1.5 \cdot b)}$

$R W A=K \cdot 12.5 \cdot E A D$

31.6 Regarding the formula set out in CRE31.5 above, $M$ is the effective maturity, calculated according to CRE32.43 to CRE32.54, and the following term is used to refer to a specific part of the capital requirements formula:

Full maturity adjustment $=\frac{(1+(M-2.5) \cdot b)}{(1-1.5 \cdot b)}$

31.7 A multiplier of 1.25 is applied to the correlation parameter of all exposures to financial institutions meeting the following criteria:

(1) Regulated financial institutions whose total assets are greater than or equal to USD100 billion. The most recent audited financial statement of the parent company and consolidated subsidiaries must be used in order to determine asset size. For the purpose of this paragraph, a regulated financial institution is defined as a parent and its subsidiaries where any substantial legal entity in the consolidated group is supervised by a regulator that imposes prudential requirements consistent with international norms. These include, but are not limited to, prudentially regulated Insurance Companies, Broker/Dealers, Banks, Thrifts and Futures Commission Merchants.

(2) Unregulated financial institutions, regardless of size. Unregulated financial institutions are, for the purposes of this paragraph, legal entities whose main business includes: the management of financial assets, lending, factoring, leasing, provision of credit enhancements, securitisation, investments, financial custody, central counterparty services, proprietary trading and other financial services activities identified by supervisors.

Correlation $=R_{-} F I=1.25 \cdot\left[0.12 \cdot \frac{\left(1-e^{-50 \cdot P D}\right)}{\left(1-e^{-50}\right)}+0.24 \cdot\left(1-\frac{\left(1-e^{-50 \cdot P D}\right)}{\left(1-e^{-50}\right)}\right)\right]$

FAQ

FAQ1 Can the Basel Committee clarify the definition of unregulated financial institutions CRE31.7? Does this could include "real" money funds such as mutual and pension funds which are, in some cases, regulated but not "supervised by a regulator that imposes prudential requirements consistent with international norms"?

For the sole purpose of CRE31.7, "unregulated financial institution" can include a financial institution or leveraged fund that is not subject to prudential solvency regulation.

## Firm-size adjustment for small or medium-sized entities (SMEs)

31.8 Under the IRB approach for corporate credits, banks will be permitted to separately distinguish exposures to SME borrowers (defined as corporate exposures where the reported sales for the consolidated group of which the firm is a part is less than $€ 50$ million) from those to large firms. A firm-size adjustment (ie $0.04 \times(1-(S-5) / 45)$ ) is made to the corporate risk weight formula for exposures to SME borrowers. S is expressed as total annual sales in millions of euros with values of $S$ falling in the range of equal to or less than $€ 50$ million or greater than or equal to $€ 5$ million. Reported sales of less than $€ 5$ million will be treated as if they were equivalent to $€ 5$ million for the purposes of the firm-size adjustment for SME borrowers.

Correlation $=R=0.12 \cdot \frac{\left(1-e^{-50 \cdot P D}\right)}{\left(1-e^{-50}\right)}+0.24 \cdot\left(1-\frac{\left(1-e^{-50 \cdot P D}\right)}{\left(1-e^{-50}\right)}\right)-0.04 \cdot\left(1-\frac{(S-5)}{45}\right)$

31.9 Subject to national discretion, supervisors may allow banks, as a failsafe, to substitute total assets of the consolidated group for total sales in calculating the SME threshold and the firm-size adjustment. However, total assets should be used only when total sales are not a meaningful indicator of firm size.

## Risk weights for specialised lending

31.10 Regarding project finance, object finance, commodities finance and income-producing real estate sub-asset classes of specialised lending (SL):

(1) Banks that meet the requirements for the estimation of PD will be able to use the foundation IRB (F-IRB) approach for the corporate asset class to derive risk weights for SL sub-classes. As specified in CRE33.2, banks that do not meet the requirements for the estimation of PD will be required to use the supervisory slotting approach.

(2) Banks that meet the requirements for the estimation of PD, LGD and EAD (where relevant) will be able to use the advanced IRB (A-IRB) approach for the corporate asset class to derive risk weights for SL sub-classes.

31.11 Regarding the high volatility commercial real estate (HVCRE) sub-asset class of specialised lending, banks that meet the requirements for the estimation of PD and whose supervisor has chosen to implement a foundation or advanced approach to HVCRE exposures will use the same formula for the derivation of risk weights that is used for other SL exposures, except that they will apply the following asset correlation formula:

Correlation $=R=0.12 \cdot \frac{\left(1-e^{-50 \cdot P D}\right)}{\left(1-e^{-50}\right)}+0.30 \cdot\left(1-\frac{\left(1-e^{-50 \cdot P D}\right)}{\left(1-e^{-50}\right)}\right)$

31.12 Banks that do not meet the requirements for estimation of LGD or EAD for HVCRE exposures must use the supervisory parameters for LGD and EAD for corporate exposures, or use the supervisory slotting approach.

## Risk-weighted assets for retail exposures that are not in default

31.13 There are three separate risk-weight functions for retail exposures, as defined in CRE31.14 to CRE31.16. Risk weights for retail exposures are based on separate assessments of PD and LGD as inputs to the risk-weight functions. None of the three retail risk-weight functions contain the full maturity adjustment component that is present in the riskweight function for exposures to banks, sovereigns and corporates. Illustrative risk weights are shown in CRE99.

## Retail residential mortgage exposures

31.14 For exposures defined in CRE30.19 that are not in default and are secured or partly secured ${ }^{1}$ by residential mortgages, risk weights will be assigned based on the following formula:

$$
\text { Correlation }=R=0.15
$$

Capital requirement $=K=\left[LGD \cdot N\left[\frac{G(PD)}{\sqrt{(1-R)}}+\sqrt{\frac{R}{1-R}} \cdot G(0.999)\right]-PD \cdot LGD\right]$

$RWA = K \cdot 12.5 \cdot EAD$

1 This means that risk weights for residential mortgages also apply to the unsecured portion of such residential mortgages.

## Qualifying revolving retail exposures

31.15 For qualifying revolving retail exposures as defined in CRE30.23 and CRE30.24 that are not in default, risk weights are defined based on the following formula:

Correlation $=R=0.04$

Capital requirement $=K=\left[LGD \cdot N\left[\frac{G(PD)}{\sqrt{(1-R)}}+\sqrt{\frac{R}{1-R}} \cdot G(0.999)\right]-PD \cdot LGD\right]$

$RWA = K \cdot 12.5 \cdot EAD$

## Other retail exposures

31.16 For all other retail exposures that are not in default, risk weights are assigned based on the following function, which allows correlation to vary with PD:

Correlation $=R=0.03 \cdot \frac{\left(1-e^{-35 \cdot P D}\right)}{\left(1-e^{-35}\right)}+0.16 \cdot\left(1-\frac{\left(1-e^{-35 \cdot P D}\right)}{\left(1-e^{-35}\right)}\right)$

Capital requirement $=K=\left[L G D \cdot N\left[\frac{G(P D)}{\sqrt{(1-R)}}+\sqrt{\frac{R}{1-R}} \cdot G(0.999)\right]-P D \cdot L G D\right]$

$R W A=K \cdot 12.5 \cdot E A D$

