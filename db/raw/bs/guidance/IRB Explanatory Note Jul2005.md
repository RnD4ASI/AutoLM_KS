# Basel Committee on Banking Supervision 

## An Explanatory Note on the Basel II IRB Risk Weight Functions

July 2005

BANK FOR INTERNATIONAL SETTLEMENTS

Requests for copies of publications, or for additions/changes to the mailing list, should be sent to:

Bank for International Settlements

Press \& Communications

$\mathrm{CH}-4002$ Basel, Switzerland

E-mail: publications@bis.org

Fax: +41 612809100 and +41612808100

© Bank for International Settlements 20054. All rights reserved. Brief excerpts may be reproduced or translated provided the source is stated.

## Table of Contents

1. Introduction ..... 1
2. Economic foundations of the risk weight formulas ..... 1
3. Regulatory requirements to the Basel credit risk model
4. Model specification ..... 4
4.1. The ASRF framework
4.2. Average and conditional PDs
4.3. Loss Given Default. ..... 6
4.4. Expected versus Unexpected Losses ..... 7
4.5. Asset correlations
4.6. Maturity adjustments
4.7. Exposure at Default and risk weighted assets ..... 11
5. Calibration of the model ..... 11
5.1. Confidence level ..... 11
5.2. Supervisory estimates of asset correlations for corporate, bank and sovereign
exposures ..... 12
5.3. Specification of the retail risk weight curves ..... 14
6. References ..... 15

## An Explanatory Note on the Basel II IRB Risk Weight Functions

## 1. Introduction

In June 2004, the Basel Committee issued a Revised Framework on International Convergence of Capital Measurement and Capital Standards (hereinafter "Revised Framework" or Basel II). ${ }^{1}$ This framework will serve as the basis for national rulemaking and implementation processes. The June 2004 paper takes account of new developments in the measurement and management of banking risks for those banks that move onto the "internal ratings-based" (IRB) approach. In this approach, institutions will be allowed to use their own internal measures for key drivers of credit risk as primary inputs to the capital calculation, subject to meeting certain conditions and to explicit supervisory approval. All institutions using the IRB approach will be allowed to determine the borrowers' probabilities of default while those using the advanced IRB approach will also be permitted to rely on own estimates of loss given default and exposure at default on an exposure-by-exposure basis. These risk measures are converted into risk weights and regulatory capital requirements by means of risk weight formulas specified by the Basel Committee.

This paper purely focuses on explaining the Basel II risk weight formulas in a non-technical way by describing the economic foundations as well as the underlying mathematical model and its input parameters. By its very nature this means that this document cannot describe the full depth of the Basel Committee's thinking as it developed the IRB framework. For further, more technical reading, references to background papers are provided.

## 2. Economic foundations of the risk weight formulas

In the credit business, losses of interest and principal occur all the time - there are always some borrowers that default on their obligations. The losses that are actually experienced in a particular year vary from year to year, depending on the number and severity of default events, even if we assume that the quality of the portfolio is consistent over time. Figure 1 illustrates how variation in realised losses over time leads to a distribution of losses for a bank:[^0]

While it is never possible to know in advance the losses a bank will suffer in a particular year, a bank can forecast the average level of credit losses it can reasonably expect to experience. These losses are referred to as Expected Losses (EL) and are shown in Figure 1 by the dashed line. Financial institutions view Expected Losses as a cost component of doing business, and manage them by a number of means, including through the pricing of credit exposures and through provisioning.

One of the functions of bank capital is to provide a buffer to protect a bank's debt holders against peak losses that exceed expected levels. Such peaks are illustrated by the spikes above the dashed line in Figure 1. Peak losses do not occur every year, but when they occur, they can potentially be very large. Losses above expected levels are usually referred to as Unexpected Losses (UL) - institutions know they will occur now and then, but they cannot know in advance their timing or severity. Interest rates, including risk premia, charged on credit exposures may absorb some components of unexpected losses, but the market will not support prices sufficient to cover all unexpected losses. Capital is needed to cover the risks of such peak losses, and therefore it has a loss-absorbing function.

The worst case one could imagine would be that banks lose their entire credit portfolio in a given year. This event, though, is highly unlikely, and holding capital against it would be economically inefficient. Banks have an incentive to minimise the capital they hold, because reducing capital frees up economic resources that can be directed to profitable investments. On the other hand, the less capital a bank holds, the greater is the likelihood that it will not be able to meet its own debt obligations, i.e. that losses in a given year will not be covered by profit plus available capital, and that the bank will become insolvent. Thus, banks and their supervisors must carefully balance the risks and rewards of holding capital.

There are a number of approaches to determining how much capital a bank should hold. The IRB approach adopted for Basel II focuses on the frequency of bank insolvencies ${ }^{2}$ arising from credit losses that supervisors are willing to accept. By means of a stochastic credit portfolio model, it is possible to estimate the amount of loss which will be exceeded with a small, pre-defined probability. This probability can be considered the probability of bank insolvency. Capital is set to ensure that unexpected losses will exceed this level of capital[^1]with only this very low, fixed probability. This approach to setting capital is illustrated in Figure 2 .

The curve in Figure 2 describes the likelihood of losses of a certain magnitude. The area under the entire curve is equal to $100 \%$ (i.e. it is the graph of a probability density). The curve shows that small losses around or slightly below the Expected Loss occur more frequently than large losses. The likelihood that losses will exceed the sum of Expected Loss (EL) and Unexpected Loss (UL) - i.e. the likelihood that a bank will not be able to meet its own credit obligations by its profits and capital - equals the hatched area under the right hand side of the curve. $100 \%$ minus this likelihood is called the confidence level and the corresponding threshold is called Value-at-Risk (VaR) at this confidence level. If capital is set according to the gap between EL and VaR, and if EL is covered by provisions or revenues, then the likelihood that the bank will remain solvent over a one-year horizon is equal to the confidence level. Under Basel II, capital is set to maintain a supervisory fixed confidence level.

So far the Expected Loss has been regarded from a top-down perspective, i.e. from a portfolio view. It can also be viewed bottom-up, namely from its components. The Expected Loss of a portfolio is assumed to equal the proportion of obligors that might default within a given time frame (1 year in the Basel context), multiplied by the outstanding exposure at default, and once more multiplied by the loss given default rate (i.e. the percentage of exposure that will not be recovered by sale of collateral etc.). Of course, banks will not know in advance the exact number of defaults in a given year, nor the exact amount outstanding nor the actual loss rate; these factors are random variables. But banks can estimate average or expected figures. As such, the three factors mentioned above correspond to the risk parameters upon which the Basel II IRB approach is built:

- $\quad$ probability of default (PD) per rating grade, which gives the average percentage of obligors that default in this rating grade in the course of one year
- $\quad$ exposure at default (EAD), which gives an estimate of the amount outstanding (drawn amounts plus likely future drawdowns of yet undrawn lines) in case the borrower defaults
- $\quad$ loss given default (LGD), which gives the percentage of exposure the bank might lose in case the borrower defaults. These losses are usually shown as a percentage
of EAD, and depend, amongst others, on the type and amount of collateral as well as the type of borrower and the expected proceeds from the work-out of the assets.

The Expected Loss (in currency amounts) can then be written as

$$
E L=P D \text { *AD * LGD }
$$

or, if expressed as a percentage figure of the EAD, as

$$
\text { EL = PD * LGD. }
$$

## 3. Regulatory requirements to the Basel credit risk model

The Basel risk weight functions used for the derivation of supervisory capital charges for Unexpected Losses (UL) are based on a specific model developed by the Basel Committee on Banking Supervision (cf. Gordy, 2003). The model specification was subject to an important restriction in order to fit supervisory needs:

The model should be portfolio invariant, i.e. the capital required for any given loan should only depend on the risk of that loan and must not depend on the portfolio it is added to. This characteristic has been deemed vital in order to make the new IRB framework applicable to a wider range of countries and institutions. Taking into account the actual portfolio composition when determining capital for each loan - as is done in more advanced credit portfolio models - would have been a too complex task for most banks and supervisors alike. The desire for portfolio invariance, however, makes recognition of institution-specific diversification effects within the framework difficult: diversification effects would depend on how well a new loan fits into an existing portfolio. As a result the Revised Framework was calibrated to well diversified banks. Where a bank deviates from this ideal it is expected to address this under Pillar 2 of the framework. If a bank failed at this, supervisors would have to take action under the supervisory review process (pillar 2).

In the context of regulatory capital allocation, portfolio invariant allocation schemes are also called ratings-based. This notion stems from the fact that, by portfolio invariance, obligorspecific attributes like probability of default, loss given default and exposure at default suffice to determine the capital charges of credit instruments. If banks apply such a model type they use exactly the same risk parameters for EL and UL, namely PD, LGD and EAD.

## 4. Model specification

## 4.1. The ASRF framework

In the specification process of the Basel II model, it turned out that portfolio invariance of the capital requirements is a property with a strong influence on the structure of the portfolio model. It can be shown that essentially only so-called Asymptotic Single Risk Factor (ASRF) models are portfolio invariant (Gordy, 2003). ASRF models are derived from "ordinary" credit portfolio models by the law of large numbers. When a portfolio consists of a large number of
relatively small exposures, idiosyncratic risks associated with individual exposures tend to cancel out one-another and only systematic risks that affect many exposures have a material effect on portfolio losses. In the ASRF model, all systematic (or system-wide) risks, that affect all borrowers to a certain degree, like industry or regional risks, are modelled with only one (the "single") systematic risk factor.

It should be noted that the choice of the ASRF for use in the Basel risk weight functions does by no means express any preference of the Basel Committee towards one model over others. Rather, the choice was entirely driven by above considerations. Banks are encouraged to use whatever credit risk models fit best for their internal risk measurement and risk management needs.

Given the ASRF framework, it is possible to estimate the sum of the expected and unexpected losses associated with each credit exposure. This is accomplished by calculating the conditional expected loss for an exposure given an appropriately conservative value of the single systematic risk factor. Under the particular implementation of the ASRF model adopted for Basel II, the conditional expected loss for an exposure is expressed as a product of a probability of default (PD), which describes the likelihood that an obligor will default, and a loss-given-default (LGD) parameter, which describes the loss rate on the exposure in the event of default.

The implementation of the ASRF model developed for Basel II makes use of average PDs that reflect expected default rates under normal business conditions. These average PDs are estimated by banks. To calculate the conditional expected loss, bank-reported average PDs are transformed into conditional PDs using a supervisory mapping function (described below). The conditional PDs reflect default rates given an appropriately conservative value of the systematic risk factor. The same value of the systematic risk factor is used for all instruments in the portfolio. Diversification or concentration aspects of an actual portfolio are not specifically treated within an ASRF model.

In contrast to the treatment of PDs, Basel II does not contain an explicit function that transforms average LGDs expected to occur under normal business conditions into conditional LGDs consistent with an appropriately conservative value of the systematic risk factor. Instead, banks are asked to report LGDs that reflect economic-downturn conditions in circumstances where loss severities are expected to be higher during cyclical downturns than during typical business conditions.

The conditional expected loss for an exposure is estimated as the product of the conditional PD and the "downturn" LGD for that exposure. Under the ASRF model the total economic resources (capital plus provisions and write-offs) that a bank must hold to cover the sum of UL and EL for an exposure is equal to that exposure's conditional expected loss. Adding up these resources across all exposures yields sufficient resources to meet a portfolio-wide Value-at-Risk target.

## 4.2. Average and conditional PDs

The mapping function used to derive conditional PDs from average PDs is derived from an adaptation of Merton's (1974) single asset model to credit portfolios. According to Merton's model, borrowers default if they cannot completely meet their obligations at a fixed assessment horizon (e.g. one year) because the value of their assets is lower than the due amount. Merton modelled the value of assets of a borrower as a variable whose value can change over time. He described the change in value of the borrower's assets with a normally distributed random variable.

Vasicek (cf. Vasicek, 2002) showed that under certain conditions, Merton's model can naturally be extended to a specific ASRF credit portfolio model. With a view on Merton's and Vasicek's ground work, the Basel Committee decided to adopt the assumptions of a normal distribution for the systematic and idiosyncratic risk factors.

The appropriate default threshold for "average" conditions is determined by applying a reverse of the Merton model to the average PDs. Since in Merton's model the default threshold and the borrower's PD are connected through the normal distribution function, the default threshold can be inferred from the PD by applying the inverse normal distribution function to the average PD in order to derive the model input from the already known model output. Likewise, the required "appropriately conservative value" of the systematic risk factor can be derived by applying the inverse of the normal distribution function to the predetermined supervisory confidence level. A correlation-weighted sum of the default threshold and the conservative value of the systematic factor yields a "conditional (or downturn) default threshold".

In a second step, the conditional default threshold is used as an input into the original Merton model and is put forward in order to derive a PD again - but this time a conditional PD. The transformation is performed by the application of the normal distribution function of the original Merton model.

In addition, the Revised Framework requires banks to undertake credit risk stress tests to underpin these calculations. Stress testing must involve identifying possible events or future changes in economic conditions that could have unfavourable effects on a bank's credit exposures and assessment of the bank's ability to withstand such changes. As a result of the stress test, banks should ensure that they have sufficient capital to meet the Pillar 1 capital requirements. The results of the credit risk stress test form part of the IRB minimum standards. Since this paper is restricted to an explanation of the risk weight formulas, no more detail of the stress testing issue is presented here.

## 4.3. Loss Given Default

Under the implementation of the ASRF model used for Basel II, the sum of UL and EL for an exposure (i.e. its conditional expected loss) is equal to the product of a conditional PD and a "downturn" LGD. As discussed earlier, the conditional PD is derived by means of a supervisory mapping function that depends on the exposure's average PD. The LGD parameter used to calculate an exposure's conditional expected loss must also reflect adverse economic scenarios. During an economic downturn losses on defaulted loans are likely to be higher than those under normal business conditions because, for example, collateral values may decline. Average loss severity figures over long periods of time can understate loss rates during a downturn and may therefore need to be adjusted upward to appropriately reflect adverse economic conditions.

The Basel Committee considered two approaches for deriving economic-downturn LGDs. One approach would be to apply a mapping function similar to that used for PDs that would extrapolate downturn LGDs from bank-reported average LGDs. Alternatively, banks could be asked to provide downturn LGD figures based on their internal assessments of LGDs during adverse conditions (subject to supervisory standards).

In principle, a function that transforms average LGDs into downturn LGDs could depend on many different factors including the overall state of the economy, the magnitude of the average LGD itself, the exposure class and the type and amount of collateral assigned to the exposure. The Basel Committee determined that given the evolving nature of bank practices in the area of LGD quantification, it would be inappropriate to apply a single supervisory LGD mapping function. Rather, Advanced IRB banks are required to estimate their own downturn LGDs that, where necessary, reflect the tendency for LGDs during economic downturn conditions to exceed those that arise during typical business conditions. Supervisors will continue to monitor and encourage the development of appropriate approaches to quantifying downturn LGDs.

The downturn LGD enters the Basel II capital function in two ways. The downturn LGD is multiplied by the conditional PD to produce an estimate of the conditional expected loss associated with an exposure. It is also multiplied by the average PD to produce an estimate of the EL associated with the exposure.


## 4.4. Expected versus Unexpected Losses

As explained above, banks are expected in general to cover their Expected Losses on an ongoing basis, e.g. by provisions and write-offs, because it represents another cost component of the lending business. The Unexpected Loss, on the contrary, relates to potentially large losses that occur rather seldomly. According to this concept, capital would only be needed for absorbing Unexpected Losses.

Nevertheless, it has to be made sure that banks do indeed build enough provisions against EL. Up to the Third Consultative Paper of the Basel Committee, banks had thus been required to include EL in the risk weighted assets as well. Provisions set aside for credit losses could be counted against the EL portion of the risk weighted assets - as such only reducing the risk weighted assets by the amount of provisions actually built. In Figure 2 above, this would have meant to hold capital for the entire distance between the VaR and the origin (less provisions).

In the end, it was decided to follow the UL concept and to require banks to hold capital against UL only. However, in order to preserve a prudent level of overall funds, banks have to demonstrate that they build adequate provisions against EL. In above Figure 2, the risk weights now relate to the distance between the VaR and the EL only.

As the ASRF model delivers the entire capital amount from the origin to the VaR in Figure 2, the EL has to be taken out of the capital requirement. The Basel II Framework accomplishes this by defining EL as the product of the bank-reported "average" PD and the bank-reported
"downturn" LGD for an exposure. Note that this definition leads to a higher EL than would be implied by a statistical expected loss concept because the "downturn" LGD will generally be higher than the average LGD. Subtracting EL from the conditional expected loss for an exposure yields a "UL-only" capital requirement.

$$
\begin{gathered}
\text { Capital requirement }(K)=\left[L G D * N\left[(1-R)^{\wedge}-0.5 * \mathrm{G}(\mathrm{PD})+(\mathrm{R} /(1-\mathrm{R}))^{\wedge} 0.5 * \mathrm{G}(0.999)\right]\right. \\
\text { EL of a loan (expressed as percentage figure of EAD) }
\end{gathered}
$$

For performing loans the Committee decided to use downturn LGDs in calculating EL. Applied for non-performing loans, this rule would result in zero capital requirements. For defaulted assets, in the risk-weight formula both the $N$ term as well as the PD would equal one, and thus the difference in the brackets equals zero (and consequently, LGD equals the EL as calculated above).

However, a capital charge for defaulted assets would be desirable in order to cover systematic uncertainty in realised recovery rates for these exposures. Therefore, the Committee determined that separate estimates of EL and LGD are needed for defaulted assets. In particular, banks are required to use their best estimate of EL, which in many cases will be lower than the downturn LGD. The difference of the downturn LGD and the best estimate of EL represents the UL capital charge for defaulted assets.

## 4.5. Asset correlations

The single systematic risk factor needed in the ASRF model may be interpreted as reflecting the state of the global economy. The degree of the obligor's exposure to the systematic risk factor is expressed by the asset correlation. The asset correlations, in short, show how the asset value (e.g. sum of all asset values of a firm) of one borrower depends on the asset value of another borrower. Likewise, the correlations could be described as the dependence of the asset value of a borrower on the general state of the economy - all borrowers are linked to each other by this single risk factor.

The asset correlations finally determine the shape of the risk weight formulas. They are asset class dependent, because different borrowers and/or asset classes show different degrees of dependency on the overall economy. Different asset correlations can also be motivated by Figure 3, which displays two stylised paths of loss experiences of different portfolios with identical expected loss (dashed-dotted horizontal line).

The loss rates of the dashed curve are subject to high variation caused by strong correlation among the individual exposures within the portfolio and with the systematic risk factor of the ASRF model. It can be interpreted as a portfolio where interactions between borrowers are high, and where borrower defaults are strongly linked to the status of the overall economy. An example for such a portfolio would be the large corporate loan book of a bank, as empirical evidence supports that the financial conditions of larger firms are closer related to the general conditions in the economy.

The loss rates of the solid curve show low variation and depend only weakly upon the systematic influence. A case of low correlation is the retail portfolio; the low correlation is a reflection of the fact that defaults of retail customers tend to be more idiosyncratic and less dependent on the economic cycle than corporate defaults. These borrowers are not strongly interlinked either. As a consequence, the loss curve is relatively flat around the EL level - the curve is less dependent on the state of the economy than the corporate curve.

The asset correlations occur in the Basel risk weight formulas:


## 4.6. Maturity adjustments

Credit portfolios consist of instruments with different maturities. Both intuition and empirical evidence indicate that long-term credits are riskier than short-term credits. As a consequence, the capital requirement should increase with maturity. Alternatively, maturity adjustments can be interpreted as anticipations of additional capital requirements due to
downgrades. Downgrades are more likely in case of long-term credits and hence the anticipated capital requirements will be higher than for short-term credits.

Economically, maturity adjustments may also be explained as a consequence of mark-tomarket (MtM) valuation of credits. Loans with high PDs have a lower market value today than loans with low PDs with the same face value, as investors take into account the Expected Loss, as well as different risk-adjusted discount factors. The maturity effect would relate to potential down-grades and loss of market value of loans. Maturity effects are stronger with low PDs than high PDs: intuition tells that low PD borrowers have, so to speak, more "potential" and more room for down-gradings than high PD borrowers. Consistent with these considerations, the Basel maturity adjustments are a function of both maturity and PD, and they are higher (in relative terms) for low PD than for high PD borrowers.

The actual form of the Basel maturity adjustments has been derived by applying a specific MtM credit risk model, similar to the KMV Portfolio Manager ${ }^{\top} \mathrm{M}$, in a Basel consistent way. This model has been fed with the same bank target solvency (confidence level) and the same asset correlations as used in the Basel ASRF model. Moreover, risk premia observed in capital market data have been used to derive the time structure of PDs (i.e. the likelihood and magnitude of PD changes). This time structure describes the probability of borrowers to migrate from one rating grade to another within a given time horizon. Thus, they are vital for modelling the potential for up- and downgrades, and consequently for deriving the maturity adjustments that result from up- and down-grades.

The output of the KMV Portfolio Manager ${ }^{T M}$-like credit portfolio model is a grid of VaR measures for a range of rating grades and maturities. It can be imagined as sketched in Figure 4. The grid contains VaR values for different PDs (1 $1^{\text {st }}$ component) and years ( $2^{\text {nd }}$ component):

Figure 4

|  | Maturity |  |  |  |  |
| :---: | :---: | :---: | :---: | :---: | :---: |
| PD grade | 1 year | 2 years | 3 years | 4 years | 5 years |
| 1 | $\operatorname{VaR}(1,1)$ | $\operatorname{VaR}(1,2)$ | $\operatorname{VaR}(1,3)$ | $\operatorname{VaR}(1,4)$ | $\operatorname{VaR}(1,5)$ |
| 2 | $\operatorname{VaR}(2,1)$ | $\operatorname{VaR}(2,2)$ | $\operatorname{VaR}(2,3)$ | $\operatorname{VaR}(2,4)$ | $\operatorname{VaR}(2,5)$ |
| 3 | $\operatorname{VaR}(3,1)$ | $\operatorname{VaR}(3,2)$ | $\operatorname{VaR}(3,3)$ | $\operatorname{VaR}(3,4)$ | $\operatorname{VaR}(3,5)$ |
| $\ldots$ | $\operatorname{VaR}(\ldots, 1)$ | $\operatorname{VaR}(. .2)$ | $\operatorname{VaR}(\ldots, 3)$ | $\operatorname{VaR}(\ldots, 4)$ | $\operatorname{VaR}(\ldots, 5)$ |

Interpreted graphically as in Figure 2, multiple distribution functions - one for each rating grade and each maturity - are derived. Importantly, the VaR in Figure 4 will be the higher the longer the maturity is.

Maturity adjustments are the ratios of each of these VaR figures to the VaR of a "standard" maturity, which was set at 2.5 years, for each maturity and each rating grade. The standard maturity was chosen with regard to the fixed maturity assumption of the Basel foundation IRB approach, which is also set at 2.5 years.

In order to derive the Basel maturity adjustment function, the grid of relative VaR figures (in relation to 2.5 years maturity) was smoothed by a statistical regression model. The regression function was chosen in such a way that

- the adjustments are linear and increasing in the maturity $\mathrm{M}$,
- the slope of the adjustment function with respect to $M$ decreases as the PD increases, and
- $\quad$ for a maturity of one year the function yields the value 1 and hence the resulting capital requirements coincide with the ones derived from the specific Basel II ASRF model as described in Section 4.1.

The maturity adjustment can be found in the Basel risk weights at the following place:

![](https://cdn.mathpix.com/cropped/2024_06_13_fb8e592dc8a15b0baf99g-15.jpg?height=459&width=1567&top_left_y=593&top_left_x=290)

The regression formula for the maturity adjustments in the Third Consultative Paper is different from the one in the Revised Framework of June 2004. This is because the VaR figures as derived by the KMV Portfolio Manager ${ }^{\top M}$-type model relate to the entire distance between the VaR and the origin in Figure 2. In the new Unexpected Loss framework, the relevant measures are the differences between the VaR and EL. Thus, the ratios between the maturity adjusted VaRs and the maturity-standardised VaR (for 2.5 years) change. The modification of the maturity adjustments is solely driven by this fact.

## 4.7. Exposure at Default and risk weighted assets

The capital requirement (K) as laid out in the Revised Framework is expressed as a percentage of the exposure. In order to derive risk weighted assets, it must be multiplied by EAD and the reciprocal of the minimum capital ratio of $8 \%$, i.e. by a factor of 12.5 :

Risk weighted assets $=12.5$ * $\mathrm{K}$ * EAD

## 5. Calibration of the model

Within the above model, two key parameters have to be determined by supervisory authorities: the confidence level supervisors feel comfortable to live with, and the asset correlation that determines the degree of dependence of the borrowers on the overall economy.

## 5.1. Confidence level

The confidence level is fixed at $99.9 \%$, i.e. an institution is expected to suffer losses that exceed its level of tier 1 and tier 2 capital on average once in a thousand years. This confidence level might seem rather high. However, Tier 2 does not have the loss absorbing capacity of Tier 1. The high confidence level was also chosen to protect against estimation errors, that might inevitably occur from banks' internal PD, LGD and EAD estimation, as well as other model uncertainties. The confidence level is included into the Basel risk weight
formulas and, as described in section 4.1, used to provide the appropriately conservative value of the single risk factor:

![](https://cdn.mathpix.com/cropped/2024_06_13_fb8e592dc8a15b0baf99g-16.jpg?height=365&width=1586&top_left_y=363&top_left_x=192)

## 5.2. Supervisory estimates of asset correlations for corporate, bank and sovereign exposures

The supervisory asset correlations of the Basel risk weight formula for corporate, bank and sovereign exposures have been derived by analysis of data sets from G10 supervisors. Some of the G10 supervisors have developed their own rating systems for corporates, and banks report corporate accounting and default data. Time series of these systems have been used to determine default rates as well as correlations between borrowers.

The analysis of these time series has revealed two systematic dependencies:

1. Asset correlations decrease with increasing PDs. This is based on both empirical evidence and intuition. Intuitively, for instance, the effect can be explained as follows: the higher the PD, the higher the idiosyncratic (individual) risk components of a borrower. The default risk depends less on the overall state of the economy and more on individual risk drivers.
2. Asset correlations increase with firm size. Again, this is based on both empirical evidence and intuition. Although empirical evidence in this area is not completely conclusive, intuitively, the larger a firm, the higher its dependency upon the overall state of the economy, and vice versa. Smaller firms are more likely to default for idiosyncratic reasons.

The asset correlation functions eventually used in the Basel risk weight formulas exhibit both dependencies:

The asset correlation function is built of two limit correlations of $12 \%$ and $24 \%$ for very high and very low PDs ( $100 \%$ and 0\%, respectively). Correlations between these limits are modelled by an exponential weighting function that displays the dependency on PD. The exponential function decreases rather fast; its pace is determined by the so-called "k-factor", which is set at 50 for corporate exposures. The upper and lower bounds for the correlations, as well as the shape of the exponentially decreasing functions, are in line with the findings of above mentioned supervisory studies.

The asset correlation function (without size adjustment) looks as follows:

Figure 5

In addition to the exponentially decreasing function of PD, correlations are adjusted to firm size, which is measured by annual sales. The linear size adjustment, shown in the above formula as $0.04 \times(1-(\mathrm{S}-5) / 45)$, affects borrowers with annual sales between $€ 5 \mathrm{mn}$ and $€ 50 \mathrm{mn}$. For borrowers with $€ 50 \mathrm{mn}$ annual sales and above, the size adjustment becomes zero, and the pure asset correlation function shown in Figure 5 applies. For borrowers with $€ 5 \mathrm{mn}$ or less annual sales, the size adjustment takes the value of 0.04 , thus lowering the
asset correlation from $24 \%$ to $20 \%$ (best credit quality) and from $12 \%$ to $8 \%$ (worst credit quality). In Figure 5, this would be shown as a parallel downward shift of the curve.

The asset correlation function for bank and sovereign exposures is the same as for corporate borrowers, only that the size adjustment factor does not apply.

## 5.3. Specification of the retail risk weight curves

The retail risk weights differ from the corporate risk weights in two respects: First, the asset correlation assumptions are different. Second, the retail risk weight functions do not include maturity adjustments. As for the other risk weight curves (see section 4.2), stress test requirements also apply to the retail portfolio.

The differences relate to the actual calibration of the curves. The asset correlations that determine the shape of the retail curves have been "reverse engineered" from (i) economic capital figures from large internationally active banks, and (ii) historical loss data from supervisory databases of the G10 countries. Both data sets contained matching PD and LGD values per economic capital or loss data point.

The banks' economic capital data have been regarded as if they were the results of the Basel risk weight formulas with their matching PD and LGD figures being inserted into the Basel risk weight formulas. Then, asset correlations that would approximately result in these capital figures within the Basel model framework, have been determined. Obviously, the asset correlation would not exactly match for each and every bank, nor for each and every PDLGD-Economic Capital triple of a given bank, but on average the figures work.

With the second data set (supervisory time series of loss data), Expected Loss (as the mean of the time series) and standard deviations of the annual losses were computed. Moreover, the Expected Loss has been split into a PD and a LGD component by using LGD estimates from supervisory charge-off data. Then again, these figures have been regarded as PD, LGD and standard deviations of the Basel risk weight model, and asset correlations that would produce approximately the same standard deviation within the Basel framework have been sought.

Both analyses showed significantly different asset correlations for different retail asset classes. They have led to the three retail risk weight curves for residential mortgage exposures, qualifying revolving retail exposures and other retail exposures, respectively. The three curves differ with respect to the applied asset correlations: relatively high and constant in the residential mortgage case, relatively low and constant in the revolving retail case, and, similarly to corporate borrowers, PD-dependent in the other retail case:

| Residential Mortgages: | Correlation $(R)=0.15$ |
| :--- | :---: |
| Qualifying Revolving Retail Exposures: Correlation $(R)=0.04$ |  |
| Other Retail Exposures: |  |
| Correlation $(R)=$ | $0.03 \times(1-\operatorname{EXP}(-35 \times \mathrm{PD})) /(1-\operatorname{EXP}(-35))+$ |
|  | $0.16 \times[1-(1-\operatorname{EXP}(-35 \times \operatorname{PD})) /(1-\operatorname{EXP}(-35))]$ |

The Other Retail correlation function is structurally equivalent to the corporate asset correlation function. However, its lowest and highest correlations are different ( $3 \%$ and $16 \%$
instead of $12 \%$ and $24 \%$ ). Moreover, the correlations decrease at a slower pace, because the "k-factor" is set at 35 instead of 50 .

In the above analysis, both the economic capital data from banks and the supervisory loss data time series implicitly contained maturity effects. Consequently, the reverse engineered asset correlations implicitly contain maturity effects as well, as the latter were not separately controlled for. In the absence of sufficient data for retail borrowers (similar to the risk premia used to deriving the time structure of PDs for corporate exposures), this control would have been difficult in any case. Thus, the maturity effects have been left as an implicit driver in the asset correlations, and no separate maturity adjustment is necessary for the retail risk weight formulas.

The implicit maturity effect also explains the relatively high mortgage correlations: not only are mortgage losses strongly linked to the mortgage collateral value and the effects of the overall economy on that collateral, but they have usually long maturities that drive the asset correlations upwards as well. Both effects are less significant with qualifying revolving retail exposures and other retail exposures, and thus the asset correlations are significantly lower.

## 6. References

Basel Committee on Banking Supervision (BCBS) (2004) International Convergence of Capital Measurement and Capital Standards. A Revised Framework. http://www.bis.org/publ/bcbsca.htm

Basel Committee on Banking Supervision (BCBS) (2003) The New Basel Capital Accord. Consultative Document.

Basel Committee on Banking Supervision (BCBS) (2001) The Internal Ratings-Based Approach. Supporting Document to the New Basel Capital Accord. Consultative Document.

Gordy, M. B. (2003) A risk-factor model foundation for ratings-based bank capital rules. Journal of Financial Intermediation 12, 199 - 232.

Merton, R. C. (1974) On the pricing of corporate debt: The risk structure of interest rates. Journal of Finance 29, 449 - 470.

Vasicek, O. (2002) Loan portfolio value. RISK, December 2002, 160 - 162.


[^0]:    1 BCBS (2004).

[^1]:    2 Insolvency here and in the following is understood in a broad sense. This includes, for instance, the case of the bank failing to meet its senior obligations.