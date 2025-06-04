## Foundations of the standardised approach for measuring counterparty credit risk exposures

This technical paper explains modelling assumptions that were used in developing the standardised approach for measuring counterparty credit risk exposures (SA-CCR). The paper also clarifies certain aspects of the SA-CCR calibration that are not discussed in the final standard that was published in March 2014 (revised April 2014). ${ }^{1}$ The language used to describe the SA-CCR in this paper may differ somewhat from the language used in the final standard. For example, the paper uses concepts that are not present in the final standard such as trade-level add-ons and single-factor subsets of hedging sets. Furthermore, it does not use the concept of effective notional, which is employed in the standard. The purpose of these adaptations is to emphasise the common aggregation framework that underpins the SA-CCR add-on formulas for different asset classes.

1 The final standard can be retrieved from http://www.bis.org/publ/bcbs279.pdf.

## 1. General structure of the SA-CCR

## 1.1 Exposure at default

The SA-CCR specifies exposure at default (EAD) measured at a netting set level. The target EAD measure for a netting set under the SA-CCR is the corresponding EAD measure under the Internal Model Method (IMM), given by the product of multiplier $\alpha$ (alpha) and Effective Expected Positive Exposure (EEPE). Under the SA-CCR, the netting-set-level EEPE is represented as the sum of two terms: the replacement cost (RC) and the potential future exposure (PFE). Thus, EAD using SA-CCR is calculated via

$$
\begin{equation*}
\mathrm{EAD}=\alpha \cdot(\mathrm{RC}+\mathrm{PFE}) \tag{1}
\end{equation*}
$$

where the multiplier alpha is set to the default IMM value, $\alpha=1.4$.

While the Current Exposure Method (CEM) also represents exposure as the sum of the RC and the PFE terms, Equation (1) differs from EAD using CEM in two important respects:

- The SA-CCR incorporates the multiplier alpha that (conceptually) converts EEPE into a loan equivalent exposure (see ISDA-TBMA-LIBA (2003); Canabarro, Picoult and Wilde (2003); and Wilde (2005)).
- The CEM specifies RC and PFE only for the unmargined case, while the SA-CCR includes formulations of RC and PFE that differ for margined and unmargined cases.

The approach to developing the SA-CCR was to simply reflect the RC and PFE for particular asset classes. RC represents a conservative estimate of the amount the bank would lose if the counterparty were to default immediately. It should be noted that margining practices are becoming more complicated over time and the approach to replacement cost reflects the diversity of margining practices that are common in the market. The PFE component reflects increases in exposure that could occur over time. PFE is related to volatility that is observed in the asset class.[^0]

## 1.2 Replacement cost

For unmargined netting sets, RC represents the loss that would occur if the counterparty defaulted immediately. Suppose that a bank has a netting set of trades with a counterparty with the current markto-market (MTM) value $V$. If the counterparty were to default immediately, the loss for the bank would be equal to the greater of $V$ and zero, ${ }^{2}$ so that $\mathrm{RC}$ is given by $\max \{V ; 0\}$.

2 See, for example, Pykhtin (2011).

There may be cases when an unmargined netting set is supported by collateral other than variation margin. All such collateral is a form of independent collateral amount (ICA) that is posted at trade inception. Generally, a bank can both receive and post ICA. Received ICA reduces the RC, as it can be used to offset losses in the event of a counterparty default. Posted ICA can be lost in the event of the counterparty default, unless it is segregated in a bankruptcy-remote account. Thus, the bank's net ICA position, or NICA, for a netting set is calculated via aggregating all received ICA with positive sign and all posted non-segregated ICA with the negative sign. Since all collateral in an unmargined netting set has the form of ICA (ie no variation margin is exchanged), the entire collateral amount is given by NICA.

The RC is obtained by subtracting the current cash-equivalent value of collateral available to the bank using a one-year horizon, $C_{\mathrm{CE}}$ (1 year), from the netting set MTM value:

$$
\begin{equation*}
\mathrm{RC}_{\text {NoMargin }}=\max \left\{V-C_{\mathrm{CE}}(1 \text { year }) ; 0\right\} \tag{2}
\end{equation*}
$$

For non-cash collateral, the cash-equivalent value $C_{\mathrm{CE}}(1$ year $)$ is obtained from the current MTM value of collateral $C_{\mathrm{MTM}}$ via application of an appropriate supervisory haircut $h(1$ year) for a one-year time horizon according to the general haircut formula:

$$
C_{\mathrm{CE}}(t)= \begin{cases}C_{\mathrm{MTM}} \cdot[1-h(t)] & \text { if } C_{\mathrm{MTM}}>0  \tag{3}\\ C_{\mathrm{MTM}} \cdot[1+h(t)] & \text { if } C_{\mathrm{MTM}}<0\end{cases}
$$

The haircut for a given time horizon accounts for a possibility of an unfavourable change of collateral value over that time horizon.

For a margined netting set, collateral generally consists of two parts: ICA (also known as initial margin) and variation margin (VM) that is posted and returned depending on the netting set MTM (see, for example, Gregory (2012, Chapter 5).

The SA-CCR sets the RC for a margined netting set equal to the maximum of the current RC and a conservative estimate of the future RC. The current RC is given by

$$
\begin{equation*}
\mathrm{RC}_{\text {Margin }}^{\text {Current }}=\max \left\{V-C_{\mathrm{CE}}(\mathrm{MPR}) ; 0\right\} \tag{4}
\end{equation*}
$$

where $C_{\mathrm{CE}}$ (MPR) is the cash-equivalent value of collateral obtained from $C_{\mathrm{MTM}}$ via application of Equation (3) with time horizon $t$ set equal to the margin period of risk (MPR). ${ }^{3}$ The future $R C$ is interpreted as the loss that could occur if the counterparty defaulted at an unknown time point within the one-year capital horizon. Because of the uncertainty of the default time, the netting set MTM value - and, therefore, the true RC - is not known. The SA-CCR conservatively assumes that, at the time of default, the netting set MTM value is high enough to trigger a margin call. This would occur at the MTM level equal to the sum[^1]of the threshold (TH) and the minimum transfer amount (MTA). If there is initial margin, the future RC is obtained by subtracting NICA from the margin call trigger level, resulting in

$$
\begin{equation*}
\mathrm{RC}_{\text {Margin }}^{\text {Fuuure }}=\max \{\mathrm{TH}+\mathrm{MTA}-\mathrm{NICA} ; 0\} \tag{5}
\end{equation*}
$$

3 MPR represents the time period over which exposure to counterparty may increase. For margined netting sets, this is the time between the last margin call that the counterparty would respond to prior its default and the closeout after the default. For unmargined trades, the time period is one year or the final maturity, consistent with the one-year time horizon generally used in the Basel accord.


By taking the maximum of Equations (4) and (5) one obtains the RC for margined netting sets:

$$
\begin{equation*}
\mathrm{RC}_{\mathrm{Margin}}=\max \left\{V-C_{\mathrm{CE}}(\mathrm{MPR}) ; \mathrm{TH}+\mathrm{MTA}-\mathrm{NICA} ; 0\right\} \tag{6}
\end{equation*}
$$

Sometimes margin agreement thresholds are set at a very high level, which would lead to unreasonably high values of the replacement cost and, therefore, the EEPE. This issue is addressed in the SA-CCR by capping the EEPE of a margined netting set by the EEPE of an otherwise equivalent unmargined netting set.

## 1.3 Potential future exposure

The SA-CCR specifies the PFE as the product of the aggregate (ie netting-set-level) add-on and a multiplier $W(\cdot)$ described in Section 5, dependent on the ratio of the netting set's current collateral-adjusted MTM value $V-C_{\mathrm{CE}}$ to the add-on itself:

$$
\begin{equation*}
\mathrm{PFE}=W\left(\frac{V-C_{\mathrm{CE}}}{\mathrm{AddOn}^{\text {aggregate }}}\right) \cdot \mathrm{AddOn}^{\text {aggregate }} \tag{7}
\end{equation*}
$$

The aggregate add-on is an estimate of the netting set EEPE under the assumptions that no collateral is currently held or posted and that the current MTM values of all trades are zero. It is generally the case that PFE is highest for at-the-money netting sets. The multiplier reduces the value of PFE when the collateral-adjusted MTM is negative.

## 2. General framework for add-ons

## 2.1 Assumptions and set-up

The netting-set-level add-on represents a conservative estimate of the EEPE of the netting set under the following assumptions:

- $\quad$ The current MTM value of each trade is zero (ie trade is at-the-money, ATM).
- The bank neither holds nor has posted collateral for the netting set.
- There are no cash flows within the capital horizon of one year.
- The evolution process for MTM value of each trade follows arithmetic Brownian motion with zero drift and fixed volatility.

These assumptions are needed to obtain the linear dependence of the aggregate add-on on a single dynamic quantity - the volatility of the netting set MTM value. The most important benefit of this dependence is that one can aggregate add-ons from a trade level to a netting-set level as if they were standard deviations. Furthermore, the SA-CCR calibration can be reduced to making assumptions on volatilities and correlations of market risk factors that drive trade MTM values.

Using these assumptions, the MTM value of trade $i$ at time $t$ can be represented as

$$
\begin{equation*}
V_{i}(t)=1_{\left\{M_{i} \geq t\right\}} \sigma_{i} \sqrt{t} X_{i} \tag{8}
\end{equation*}
$$

where $1_{\{\}\}}$is the indicator function of a Boolean variable (it takes a value of 1 if the argument is TRUE and value of 0 otherwise), $M_{i}$ is the remaining maturity, $\sigma_{i}$ is the volatility of the MTM value of trade $i$ and $X_{i}$ is a standard normal random variable.

Suppose that we know the correlations $r_{i j}$ between random variables $X_{i}$ and $X_{j}$. Then, the MTM value $V(t)$ of a netting set at time $t$ can be expressed via

$$
\begin{equation*}
V(t)=\sigma(t) \sqrt{t} Y \tag{9}
\end{equation*}
$$

where $Y$ is a standard normal random variable and $\sigma(t)$ is the annualised normal volatility of the netting set at time $t$ given by

$$
\begin{equation*}
\sigma(t)=\left[\sum_{i, j} 1_{\left\{M_{i} \geq t\right\}} 1_{\left\{M_{j} \geq t\right\}} r_{i j} \sigma_{i} \sigma_{j}\right]^{\frac{1}{2}} \tag{10}
\end{equation*}
$$

Note that, in spite of the assumption of fixed annualised volatility for MTM value of each trade, the annualised volatility $\sigma(t)$ of the netting set generally depends on time $t$ because trades that mature before time $t$ do not contribute to $\sigma(t)$.

## 2.2 Add-ons for unmargined netting sets

Expected exposure (EE) can be calculated for an unmargined netting set:

$$
\begin{equation*}
\operatorname{EE}^{\text {no-margin }}(t)=\mathrm{E}[\max \{\sigma(t) \sqrt{t} Y, 0\}]=\varphi(0) \sigma(t) \sqrt{t} \tag{11}
\end{equation*}
$$

where $\varphi(\cdot)$ is the standard normal probability density, so $\varphi(0)=1 / \sqrt{2 \pi}$. This value represents the average exposure of the netting set at time $t$. Cases where the netting set value is negative represent situations where the bank owes the counterparty and so the exposure is set to zero.

Conceptually, the unmargined aggregate add-on should be defined as the EEPE calculated from the EE profile of Equation (11). However, this would require calculating $\sigma(t)$ at several time points between zero and one year. To avoid this complexity, the consultative paper BCBS (2013) floored the remaining maturity of all trades by one year. ${ }^{4}$ The maturity floor is equivalent to replacing $\sigma(t)$ with $\sigma(0)$ in Equation (11) whenever $t \leq 1$ year, which allows one to calculate the EEPE from Equation (11) in closed form:

$$
\begin{equation*}
\operatorname{AddOn}_{\text {aggregate }}^{\text {no-margin }}=\frac{1}{1 \text { year }} \int_{0}^{1 \text { year }} \mathrm{EE}^{\text {no-margin }}(t) d t=\frac{2}{3} \varphi(0) \sigma(0) \sqrt{1 \text { year }} \tag{12}
\end{equation*}
$$

Note that Equation (12) can be restated in terms of aggregation of trade-level add-ons rather than aggregation of trade-level volatilities:

$$
\begin{equation*}
\operatorname{AddOn}_{\text {aggregate }}^{\text {no-margin }}=\left[\sum_{i, j} \mathrm{r}_{i j} \operatorname{AddOn}_{i}^{\text {no-margin }} \mathrm{AddOn}_{j}^{\text {no-margin }}\right]^{\frac{1}{2}} \tag{13}
\end{equation*}
$$

where add-on of trade $i$ represents the EEPE of a netting set consisting of only trade $i$ :

$$
\begin{equation*}
\operatorname{AddOn}_{i}^{\text {no-margin }}=\frac{2}{3} \varphi(0) \sigma_{i} \sqrt{1 \text { year }} \tag{14}
\end{equation*}
$$

However, application of the one-year floor would result in unreasonably high trade-level addons for short-term trades. In particular, short-term trades would have a capability to offset long-term trades to a much greater extent that they should. ${ }^{5}$ To prevent this, the definition of the aggregate add-on for unmargined netting sets was kept in the form of Equation (13), but the definition of trade-level addon was changed to accommodate maturities shorter than one year:

$$
\begin{equation*}
\operatorname{AddOn}_{i}^{\mathrm{nomargin}}=\frac{2}{3} \varphi(0) \sigma_{i} \sqrt{1 \text { year }} \mathrm{MF}_{i}^{\mathrm{no}-\text { margin }} \tag{15}
\end{equation*}
$$

where maturity factor $\mathrm{MF}_{i}^{\text {no-margin }}$ is defined as

$$
\begin{equation*}
\mathrm{MF}_{i}^{\text {no-margin }}=\sqrt{\frac{\min \left\{M_{i}, 1 \text { year }\right\}}{1 \text { year }}} \tag{16}
\end{equation*}
$$

scales down the volatility of the trade MTM from one year to the trade remaining maturity $M_{i}$ for the trades with $M_{i}<1$ year.

5 For example, to fully offset the risk of a one-year FX forward, it would be sufficient to book a very short-term FX forward or an FX spot contract of the same notional in the opposite direction.

## 2.3 Add-ons for margined netting sets

For margined netting sets, the SA-CCR add-on is defined (in the spirit of the IMM Shortcut Method) as the expected increase of the netting set MTM over the MPR. ${ }^{6}$ Since the portfolio is assumed to have the current MTM equal to zero, the add-on for a margined netting set defined in this manner reduces to the value of the $E E$ of an otherwise equivalent unmargined netting set at the time point equal to the MPR:

$$
\begin{equation*}
\operatorname{AddOn}_{\text {agrregate }}^{\text {margin }}=\mathrm{EE}^{\text {no-margin }}(\mathrm{MPR})=\varphi(0) \cdot \sigma(0) \sqrt{\mathrm{MPR}} \tag{17}
\end{equation*}
$$

Similarly, for a margined netting set containing only trade $i$, the add-on is

$$
\begin{equation*}
\operatorname{AddOn}_{i}^{\text {margin }}=\varphi(0) \sigma_{i} \sqrt{\mathrm{MPR}} \tag{18}
\end{equation*}
$$

Thus, one can replace aggregation of trade-level volatilities with aggregation of trade-level addons for both margined and unmargined netting sets via Equation (13) that we restate here for margined netting sets:

$$
\operatorname{AddOn}_{\text {aggregate }}^{\text {margin }}=\left[\sum_{i, j} \mathrm{r}_{i j} \operatorname{AddOn}_{i}^{\text {margin }} \operatorname{AddOn}_{j}^{\text {margin }}\right]^{\frac{1}{2}}
$$

Finally, trade-level margined add-ons in Equation (18) can be restated in exactly the same form as trade-level non-margin add-ons in Equation (15)

$$
\begin{equation*}
\operatorname{AddOn}_{i}^{\text {margin }}=\frac{2}{3} \varphi(0) \sigma_{i} \sqrt{1 \text { year }} \mathrm{MF}_{i}^{\text {margin }} \tag{19}
\end{equation*}
$$

with differently defined maturity factors:[^2]

$$
\begin{equation*}
\mathrm{MF}_{i}^{\text {margin }}=\frac{3}{2} \sqrt{\frac{\mathrm{MPR}}{1 \text { year }}} \tag{20}
\end{equation*}
$$

Thus, the entire difference between margined and unmargined trade-level add-ons resides in the maturity factors. Because of this, there will be no distinction made between margined and unmargined netting sets in the remainder of this paper when add-ons are discussed.

6 See BCBS (2006) and BCBS (2010). See also analysis in Gibson (2005) where the IMM Shortcut Method was first proposed.

## 3. Structure of add-on calculations

For the purpose of the add-on calculation, each trade in the netting set is assigned to at least one of five asset classes: interest rate (IR), foreign exchange (FX), credit, equities and commodities. The designation should be made according to the nature of the primary risk factor (eg IR for most single currency IR swaps, FX for most cross-currency swaps, credit for most credit default swaps). For more complex trades, where it is difficult to determine a single primary risk factor, bank supervisors may require that trades be allocated to more than one asset class.

While the SA-CCR add-on formulas are asset class-specific, there are a number of common features for all asset classes. Most importantly, netting-set-level add-ons are calculated from trade-level add-ons via an aggregation procedure based on the general principles outlined in the previous section.

## 3.1 Trade-level add-ons

The SA-CCR does not directly operate with trade volatilities. Instead, the directional add-on $\mathrm{AddOn}_{i}^{\text {(trade) }}$ for each trade $i$ of asset class $a$ is given by the product of the following four quantities: directional delta $\delta_{i}$, adjusted notional $d_{i}^{(a)}$, supervisory factor $\mathrm{SF}_{i}^{(a)}$ and maturity factor $\mathrm{MF}_{i}$ :

$$
\begin{equation*}
\operatorname{AddOn}_{i}^{\text {(trade) }}=\delta_{i} d_{i}^{(a)} \mathrm{SF}_{i}^{(a)} \mathrm{MF}_{i} \tag{21}
\end{equation*}
$$

where maturity factor $\mathrm{MF}_{i}$ is defined via Equation (16) for unmargined trades and via Equation (20) for margined trades. Equation (21) is meant to be equivalent to Equations (15) and (19) with one difference: add-ons in Equation (21) can be negative. Negative add-ons are a means of accommodating negative correlations $r_{i j}$ in Equation (13) without using negative correlations explicitly. Comparing Equation (21) with Equations (15) and (19) reveals that the SA-CCR approximates the trade-level volatility via

$$
\begin{equation*}
\sigma_{i}=\frac{3 \mathrm{SF}_{i}^{(a)}}{2 \varphi(0)} \cdot\left|\delta_{i}\right| \cdot d_{i}^{(a)} \tag{22}
\end{equation*}
$$

where the first factor (the ratio) can be interpreted as the standard deviation of the primary risk factor at the one-year horizon.

The quantities that appear in Equation (21) are specified in the final standard for the SA-CCR. They have the following meaning:

- Directional delta $\delta_{i}$ : Delta serves two purposes: it specifies the direction of the trade with the respect to the primary risk factor (positive for long, and negative for short) and serves as the scaling factor for trades that are non-linear in the primary risk factor. Banks' internal deltas are not allowed; standardised values are used instead. Trades that are not options or CDOs are assumed to be linear in the underlying risk factor and have delta of unit magnitude. For options, banks should use the Black-Scholes formula for delta as provided in the final standard. For CDOs,
a standardised formula provided in the standard text should be used with internal attachment and detachment points (this formula is discussed later in this paper).
- Adjusted notional $d_{i}^{(a)}$ : While the definition of adjusted notional is asset class-specific, one can generally state that adjusted notional quantifies the size of the trade. It is proportional to either a trade's notional (as in the case of IR, FX and credit) or the current price of the underlying assets (as in the case of equity and commodity). For IR and credit derivatives, the adjusted notional is also proportional to the supervisory duration.
- $\quad$ Supervisory factor $\mathrm{SF}_{i}^{(a)}$ : The supervisory factor is the supervisory value of EEPE of a netting set consisting of a single linear trade (ie unit delta) of unit adjusted notional belonging to the same subclass of asset class $a$ as trade $i$. Supervisory factors incorporate the volatility assumed by regulators for the primary risk factor. While the final standard specifies supervisory factors at specific subclasses within each asset class, conceptually the SA-CCR structure is very flexible: the method can be easily made more or less granular without changing the structure of the approach.


## 3.2 Add-on aggregation

Aggregation of trade-level add-ons to the netting set level is done by imposing a certain structure on the correlation matrix $r_{i j}$ in the aggregation formula given by Equation (13). A key add-on aggregation concept of the SA-CCR is the notion of a hedging set. By definition, a hedging set is the largest collection of trades of a given asset class within a netting set for which netting benefits are recognised in the PFE add-on of the SA-CCR. No netting is recognised across hedging sets, so a netting-set-level add-on is calculated as a direct sum of the absolute values of hedging-set-level add-ons:

$$
\begin{equation*}
\operatorname{AddOn}^{(\text {no-margin })}=\sum_{m}\left|\operatorname{AddOn}_{m}^{(\mathrm{HS})}\right| \tag{23}
\end{equation*}
$$

where $\mathrm{AddOn}_{m}^{(\mathrm{HS})}$ is the add-on for hedging set $m$. Equation (23) is equivalent to assuming perfect positive correlation between hedging set MTM values.

Hedging-set-level add-ons are obtained via the following two-step aggregation process that recognises netting within each hedging set. All trades of a hedging set are designated to single-factor subsets. It is assumed that all trades of a given single-factor subset are driven by the same market factor, so full offset is allowed for such trades:

$$
\begin{equation*}
\operatorname{AddOn}_{j}^{(\mathrm{SFS})}=\sum_{i \in \mathrm{SFS}_{j}} \mathrm{AddOn}_{i}^{(\text {trade })} \tag{24}
\end{equation*}
$$

where $\mathrm{AddOn}_{i}^{\text {(trade) }}$ is the directional add-on (ie add-ons for long and short trades have opposite signs) for trade $i$ described above and notation $i \in \mathrm{SFS}_{j}$ should be interpreted as all trades belonging to singlefactor subset $j$ of a given hedging set.

Single-factor subsets are further aggregated to a hedging-set level under the assumption that, within a hedging set, risk factors driving single-factor subsets are imperfectly correlated:

$$
\begin{equation*}
\operatorname{AddOn}_{m}^{(\mathrm{HS})}=\left[\sum_{j, k \in \mathrm{HS}_{m}} \rho_{j k} \cdot \operatorname{AddOn}_{j}^{(\mathrm{SFS})} \cdot \operatorname{AddOn}_{k}^{(\mathrm{SFS})}\right]^{\frac{1}{2}} \tag{25}
\end{equation*}
$$

where notation $j, k \in \mathrm{HS}_{m}$ should be interpreted as all pairs of single-factor subsets belonging to the same hedging set $m$ of a given asset class, and correlations $\rho_{j k}$ are prescribed by regulators.

The next section describes asset-class-specific aspects of the general framework outlined above. These aspects include the definition of adjusted notional along with the specification of hedging sets, single-factor subsets and correlation parameters.

## 4. Add-on calculations by asset class

## 4.1 Interest rate

Consider a fixed-for-floating IR swap as the most common example of an IR derivative. Suppose that swap $i$ payments start at time $S_{i}$, end at time $E_{i}$ and refer to notional $N_{i}(t)$ at time $t$. In the continuous limit, swap MTM value can be written as

$$
\begin{equation*}
V_{i}^{\text {swap }}(t)=\left[\mathrm{SR}_{i}(t)-\mathrm{FR}_{i}\right] \int_{\max \left\{\mathcal{S}_{i}, t\right\}}^{E_{i}} N_{i}(\tau) \mathrm{DF}(t, \tau) d \tau \tag{26}
\end{equation*}
$$

where $\mathrm{SR}_{i}(t)$ is the swap rate at time $t$, FR is the fixed rate and $\mathrm{DF}(t, \tau)$ is the discount factor from time $\tau$ to time $t$. The SA-CCR assumes that all variability of the swap MTM value results from changes of the swap rate, thus "freezing" the discount factor in the integral. The IR supervisory factor is meant to capture the one-year volatility of the swap rate, while the adjusted notional is meant to represent the value of the integral in Equation (26) at time $t=0$. The SA-CCR approximates the integral by setting the adjusted notional equal to

$$
\begin{equation*}
d_{i}^{(\mathbb{R})}=\bar{N}_{i} \cdot \mathrm{SD}_{i} \tag{27}
\end{equation*}
$$

where $\bar{N}_{i}$ is the average of the swap notional over the remaining life of the swap payments and $\mathrm{SD}_{i}$ is the supervisory duration given by

$$
\begin{equation*}
\mathrm{SD}_{i}=\int_{S_{i}}^{E_{i}} \exp (-r t) d t=\frac{\exp \left(-r S_{i}\right)-\exp \left(-r E_{i}\right)}{r} \tag{28}
\end{equation*}
$$

with the interest rate set to $r=0.05$.

Interest rate hedging sets are specified as all IR trades of a netting set denominated in the same currency. Three single-factor subsets of a hedging set are defined via the range of the end date: (1) $E_{i} \leq 1$ year ; (2) 1 year $<E_{i} \leq 5$ years ; (3) $E_{i}>5$ years. Thus, Equation (24) specifies the add-ons for each of the three maturity buckets of a given currency. Correlations between the maturity buckets are set as follows: $\rho_{12}=\rho_{23}=70 \%$ and $\rho_{13}=30 \%$ (calibration of these correlations is discussed later in this paper). Thus, in the case of $\mathrm{IR}$, Equation (25) becomes:

$$
\begin{align*}
& \mathrm{AddOn}_{m}^{(\mathrm{CCY})}=\left[\left(\mathrm{AddOn}_{1}^{(\mathrm{MB})}\right)^{2}+\left(\mathrm{AddOn}_{2}^{(\mathrm{MB})}\right)^{2}+\left(\operatorname{AddOn}_{3}^{(\mathrm{MB})}\right)^{2}\right. \\
& \left.+1.4 \cdot \mathrm{AddOn}_{1}^{(\mathrm{MB})} \cdot \mathrm{AddOn}_{2}^{(\mathrm{MB})}+1.4 \cdot \mathrm{AddOn}_{2}^{(\mathrm{MB})} \cdot \mathrm{AddOn}_{3}^{(\mathrm{MB})}+0.6 \cdot \mathrm{AddO}_{1}^{(\mathrm{MB})} \cdot \mathrm{AddOn}_{3}^{(\mathrm{MB})}\right]^{\frac{1}{2}} \tag{29}
\end{align*}
$$

where the notation "CCY" indicates that the hedging set is a currency and the notation "MB" indicates that the single-factor subsets are maturity buckets.

## 4.2 Foreign exchange

Consider a linear FX trade such as an FX forward between a foreign currency and the domestic currency. Assuming that the forward maturity is greater than one year (smaller maturities are accounted by maturity factors), volatility of the forward's MTM value over the one-year horizon is independent of the forward's maturity and is given by the product of the notional of the foreign leg converted to the domestic currency using the current FX spot rate and the one-year relative volatility of the FX spot rate. This example motivates specifying the adjusted notional according to ${ }^{7}$

$$
\begin{equation*}
d_{i}^{(\mathrm{FX})}=N_{i}^{\text {foreign }} \tag{30}
\end{equation*}
$$

where $N_{i}^{\text {foreign }}$ is the current value of the notional of the foreign currency leg of trade $i$ measured in the domestic currency. If both legs of a trade are in different foreign currencies, a conservative simplification is applied: Equation (30) should be calculated for both legs, and the maximum should be chosen.

An FX hedging set is specified as all trades of a netting set referencing the same pair of currencies. It is assumed that all FX trades of the same hedging set are driven by the same market factor, which is the FX spot rate for the hedging set's currency pair. Thus, Equation (24) aggregates all trades of a given currency pair, and Equation (25) reduces to taking the absolute value of the single single-factor add-on: $\mathrm{AddOn}_{m}^{(\mathrm{CCY}}$ pair) $=\left|\operatorname{AddOn}_{1}^{(\mathrm{SFS})}\right|$. When delta for $\mathrm{FX}$ trades is calculated, the trade direction within each currency pair must be consistent (eg positive for all trades long GBP/EUR and negative for all trades short GBP/EUR).

7 One can show that this specification is appropriate for another common example of FX linear trades - cross-currency swap.

## 4.3 Credit

MTM value of the most popular credit derivative, single-name or index credit default swap (CDS), can be represented in the form similar to Equation (26):

$$
\begin{equation*}
V_{i}^{\mathrm{CDS}}(t)=\left[\mathrm{CS}_{i}(t)-\mathrm{CS}_{i}^{\mathrm{contr}}\right] \int_{\max \left\{S_{i}, t\right\}}^{E_{i}} N_{i}(\tau) \mathrm{DF}(t, \tau)\left[1-\mathrm{EL}_{i}(t, \tau)\right] d \tau \tag{31}
\end{equation*}
$$

where $\mathrm{CS}_{i}(t)$ is the credit spread at time $t, \mathrm{CS}_{i}^{\text {contr }}$ is the contractual credit spread and $\mathrm{EL}_{i}(t, \tau)$ is the risk-neutral expected loss due to default(s) between time $t$ and time $\tau$ per unit of notional. ${ }^{8}$ The supervisory factors for credit derivatives account for the one-year volatility of the credit spread. The adjusted notional for credit derivatives is meant to represent the value of the integral in Equation (31) at time $t=0$. It was decided to ignore the difference between the integrals in Equations (26) and (31) and set the adjusted notional for credit derivatives equal to the one for IR derivatives given by Equations (27) and (28).

All credit trades of a given netting set represent a single hedging set. A single-factor subset is specified as all credit trades referencing the same entity (which can be either a single name or an index). Thus, Equation (24) aggregates all credit trades in a netting set that reference the same entity. Aggregation across entities is done assuming that each entity is driven by a single systematic risk factor and an idiosyncratic risk factor. The systematic factor loading for entity $j$ is quantified via correlation $\rho_{j}$ between the full stochastic driver of credit spread of entity $j$ and the systematic factor. This correlation is set to $50 \%$ for entities that are single names and to $80 \%$ for those that are indices. The pairwise correlation between two distinct entities $j$ and $k$ is given by the product $\rho_{i} \rho_{k}$ and can have the following values:[^3]$25 \%$ between two single names; $40 \%$ between a single name and an index; $64 \%$ between two indices. Applying the single-factor assumption to Equation (25) results in the following add-on aggregation formula:

$$
\begin{equation*}
\operatorname{AddOn}_{\mathrm{CD}}=\left(\left[\sum_{j} \rho_{j} \cdot \operatorname{AddOn}_{j}^{(\text {Entity })}\right]^{2}+\sum_{j}\left(1-\rho_{j}^{2}\right) \cdot\left(\operatorname{AddOn}_{j}^{(\text {Entity })}\right)^{2}\right)^{\frac{1}{2}} \tag{32}
\end{equation*}
$$

The key features of credit derivatives that are captured are the maturity aspect and the basis risk. The single-factor model reflects the fact that, although credit spreads in general move together, there can be considerable idiosyncratic variation in a single name that limits the benefits of hedging a long CDS with one reference name with a short CDS referencing a different name. This strikes a balance between recognising diversification (which is greatest when correlation is zero) and hedging of dissimilar names (which is greatest when correlation is one).

8 In the case of single-name $\mathrm{CDS}_{1} \mathrm{EL}_{i}(t, \tau)$ is the risk-neutral cumulative probability of default between $t$ and $\tau$.

## 4.4 Equities

For the simplest linear equity derivatives, such as equity forwards, volatility of the trade MTM value is equal to the product of the volatility of the stock (index) price and the number of units of stock (index) referenced by the trade. The volatility of the equity price can be approximated by the product of the current stock (index) price and the relative volatility of the stock (index) price. The supervisory factors for equity derivatives are meant to capture the relative volatility of the stock (index) price, while the adjusted notional is set equal to the product to the current stock (index) price and the number of units referenced by the trade.

Aggregation of equity derivatives is done in exactly the same manner as aggregation of credit derivatives. It is assumed that all trades in a netting set referencing the same entity (single name or index) are driven by the same factor, so Equation (24) is applied at an entity level. It is further assumed that stock prices and equity index values are driven by a single systematic factor with the same correlation values as for credit derivatives: $50 \%$ single names and to $80 \%$ for those that are indices. Thus, Equation (32) is used for aggregation of equity derivatives across entities.

This design captures the tendency of equity markets to move together, but limits the ability of different names to offset. Here again, a balance was struck between recognising diversification benefits and hedging benefits.

## 4.5 Commodities

For commodity derivatives, the arguments with respect to the volatility of the MTM value of linear contracts are similar to those used for equity derivatives above. The supervisory factors for commodity derivatives are meant to capture the relative volatility of the commodity price, while the adjusted notional is defined as the product of the current unit price (eg one barrel of oil) of the commodity referenced by the trade and the number of units referenced by the trade.

A commodity hedging set is specified as all trades of a netting set referencing the same broad category of commodity: energy, metals, agricultural, or other commodity. Single-factor subsets are specified as a specific commodity type: electricity, oil, gas, nickel, corn. Aggregation within commodity types is done via Equation (24). Specific commodity types are aggregated to a hedging set level using the same single-factor model that is used for credit and equity derivatives, but with the correlation parameter set to $40 \%$ for all commodity types. This results in the use of Equation (32), but interpreting $j$ as a specific commodity type with $\rho_{j}$ set to $40 \%$ for all $j$.

## 5. Multiplier

Recall that a netting-set-level add-on is an estimate of the netting set PFE under the four assumptions stated in Section 2.1 of this paper: current MTM and collateral are equal to zero; there are no cash flows within the horizon; MTM follows zero-drift Brownian motion. Let us examine what would happen to the netting set PFE when the first two assumptions are relaxed, so that non-zero current MTM and collateral are allowed.

Let us consider a margined netting set. Generally, EE of a margined netting set is characterised by a full term structure calculated from ${ }^{9}$

$$
\begin{equation*}
\mathrm{EE}^{\operatorname{margin}}(t)=\mathrm{E}[\max \{V(t)-C(t), 0\}] \tag{33}
\end{equation*}
$$

where $V(t)$ is the MTM value of the netting set at time $t$ and $C(t)$ is the collateral available to the bank at time $t$. The SA-CCR does not attempt to model collateral dynamics through time and simply takes a single point $t=$ MPR from the EE profile as the measure of exposure. Furthermore, the SA-CCR assumes that collateral is not exchanged during the MPR, so only non-cash collateral can change value over the MPR due to volatility of the collateral asset. The volatility of non-cash collateral is not modelled either: instead, a haircut is applied to the current collateral value $C_{\mathrm{MTM}}$ to obtain a deterministic cash-equivalent value $C_{\mathrm{CE}}$ (MPR), as described by Equation (3). Thus, the SA-CCR target measure of exposure for margined netting sets is

$$
\begin{equation*}
\mathrm{EE}^{\operatorname{margin}}(\mathrm{MPR})=\mathrm{E}\left[\max \left\{V(\mathrm{MPR})-C_{\mathrm{CE}}(\mathrm{MPR}), 0\right\}\right] \tag{34}
\end{equation*}
$$

Under the assumption that a netting set's MTM follows a driftless Brownian motion, the value of the MTM at the MPR can be described via

$$
\begin{equation*}
V(\mathrm{MPR})=V+\sigma(0) \sqrt{\mathrm{MPR}} Y \tag{35}
\end{equation*}
$$

where $\sigma(0)$ is the volatility of the netting set MTM value at time 0 (ie counting all trades in the netting set) and $Y$ is a standard normal random variable. ${ }^{10}$ Substituting Equation (35) into Equation (34), calculating the expectation analytically results in:

$$
\begin{align*}
\mathrm{EE}^{\text {margin }}(\mathrm{MPR}) & =\left[V-C_{\mathrm{CE}}(\mathrm{MPR})\right] \Phi\left(\frac{V-C_{\mathrm{CE}}(\mathrm{MPR})}{\sigma(0) \sqrt{\mathrm{MPR}}}\right)  \tag{36}\\
& +\sigma(0) \sqrt{\mathrm{MPR}} \varphi\left(\frac{V-C_{\mathrm{CE}}(\mathrm{MPR})}{\sigma(0) \sqrt{\mathrm{MPR}}}\right)
\end{align*}
$$

where $\Phi(\cdot)$ is the standard normal cumulative distribution function. The margined add-on in the form of Equation (17) is obtained from Equation (36) by setting $V-C_{\mathrm{CE}}(\mathrm{MPR})=0$ :

$$
\mathrm{AddOn}_{\text {aggregate }}^{\text {margin }}=\varphi(0) \sigma(0) \sqrt{\mathrm{MPR}}
$$

To obtain the PFE, one needs to subtract the current replacement cost from the right-hand side of Equation (36). However, the SA-CCR does not give any credit to PFE reduction when the replacement cost is positive (ie $\mathrm{PFE}^{\text {margin }}=\mathrm{AddOn}_{\text {aggregate }}^{\text {maryin }}$ whenever $V-C_{\mathrm{CE}}(\mathrm{MPR}) \geq 0$ ). For the $V-C_{\text {CE }}(\mathrm{MPR})<0$ case, Equation (36) produces the PFE because the current replacement cost is zero.[^4]

To derive the SA-CCR multiplier, we need to express the PFE in terms of add-on rather than volatility. This is easily achieved by using Equation (17) to express $\sigma(0)$ in terms of the margined add-on in Equation (36):

$$
\begin{align*}
\mathrm{PFE}^{\text {margin }}= & {\left[V-C_{\mathrm{CE}}(\mathrm{MPR})\right] \cdot \Phi\left(\varphi(0) \frac{V-C_{\mathrm{CE}}(\mathrm{MPR})}{\mathrm{AddOn}_{\text {aggregate }}^{\text {margin }}}\right) } \\
& +\frac{\text { AddOn }_{\text {aggregate }}^{\text {margin }}}{\varphi(0)} \cdot \varphi\left(\varphi(0) \frac{V-C_{\mathrm{CE}}(\mathrm{MPR})}{\mathrm{AddOn}_{\text {aggregate }}^{\text {margin }}}\right) \tag{37}
\end{align*}
$$

where Equation (37) is valid only for the $V-C_{\mathrm{CE}}(\mathrm{MPR})<0$ case.

10 See Section 2.

By definition, the multiplier is the ratio of the PFE to the add-on. Combining the positive and negative collateralised MTM cases and using a shorthand notation $y=\left[V-C_{\mathrm{CE}}(\mathrm{MPR})\right] /$ AddOn

$$
\begin{equation*}
W_{\text {model }}(y)=\min \left\{1, y \Phi[\varphi(0) y]+\frac{\varphi[\varphi(0) y]}{\varphi(0)}\right\} \tag{38}
\end{equation*}
$$

This function is shown by the dash-double-dotted curve in Figure 1.

The multiplier in Equation (38) is based on the assumption that the netting set future MTM value is normally distributed. However, MTM values of real netting sets are likely to exhibit heavier tail behaviour than the one of the normal distribution. To account for this possibility, a more conservative multiplier function was chosen:

$$
\begin{equation*}
W_{\mathrm{exp}}(y)=\min \left\{1, \exp \left(\frac{y}{2}\right)\right\} \tag{39}
\end{equation*}
$$

where the factor of 2 appears in the denominator in order to match the slope of $W_{\text {model }}(y)$ at $y=0$. This function is shown by the dash-dotted curve in Figure 1.

While the exponential multiplier in Equation (39) is significantly more conservative than the model-based multiplier in Equation (38), concerns were raised that the multiplier would still approach zero with infinite overcollateralisation. To address this concern, a floor $F$ was added to the exponential multiplier in a manner that preserves the function slope at the origin:

$$
\begin{equation*}
W_{\mathrm{SA}-\mathrm{CCR}}(y)=\min \left\{1, F+(1-F) \exp \left(\frac{y}{2(1-F)}\right)\right\} \tag{40}
\end{equation*}
$$

The solid curve in Figure 1 shows this function with $F=5 \%$ currently chosen in the SA-CCR.

Figure 1: The dependence of multiplier on $\left(V-C_{\mathrm{CE}}\right) /$ AddOn

To apply the normal approximation to unmargined netting sets on a consistent basis, one has to calculate the EEPE as the time average (between zero and one year) of the following EE profile:

$$
\begin{equation*}
\mathrm{EE}(t)=\left[V-C_{\mathrm{CE}}(t)\right] \cdot \Phi\left(\frac{V-C_{\mathrm{CE}}(t)}{\sigma(t) \sqrt{t}}\right)+\sigma(t) \sqrt{t} \cdot \varphi\left(\frac{V-C_{\mathrm{CE}}(t)}{\sigma(t) \sqrt{t}}\right) \tag{41}
\end{equation*}
$$

Unfortunately, such averaging is possible in closed form only for the trivial case $V-C_{\mathrm{CE}}(t)=0$ that was used in Equation (12). To circumvent this difficulty, the SA-CCR applies the same multiplier function in Equation (40) to both margined and unmargined cases, with function argument $y$ for nonmargined netting sets defined in the same way as for margined netting sets, but using an unmargined aggregate add-on and one-year horizon for collateral haircut: $y=\left[V-C_{\mathrm{CE}}(1\right.$ year $\left.)\right] / \mathrm{AddOn}_{\text {aggregate }}^{\text {no-margin }}$

The multiplier formulation recognises that the PFE portion of EEPE is smaller the further one moves away from an ATM netting set. It is conservative in this regard in three ways. First, it incorporates fat tails through the use of the exponential function. Second, a floor is placed on the value of the multiplier to ensure that some PFE is always recognised. Third, the multiplier only reduces PFE for negative MTM values, but does not recognise possible reduction of PFE for positive MTM values.

9 See, for example, Pykhtin (2010).


## 6. Calibration

Calibration of supervisory factors and single-systematic-factor correlations was done based on four calibration exercises. First, the supervisory factors were calculated from asset class volatilities using Equation (22). However, these initial calibrations were based on volatility estimates averaged from a wide variety of trades within an asset class. Then, these calibrations were compared to simulation models of small portfolios of trades for each asset class. The simulation models used were developed by supervisors
and banks' own IMM models. Lastly, to ensure that the SA-CCR was applicable to large portfolios, a quantitative impact study was conducted where banks compared the results for their own portfolios using SA-CCR, IMM and CEM. The final calibration considers the results of all of these exercises. The final parameter calibrations are provided in the final standards text. The rest of this section will focus on two specific aspects of the SA-CCR calibration: correlations between IR maturity buckets and deltas for CDO tranches.

## 6.1 Correlations between IR maturity buckets

Generally, the correlation between MTM values of two IR trades referencing the same IR curve depends on four time parameters: the start and end dates of either trade as they are defined in Section 4.1 of this paper. However, this four-dimensional problem is not tractable within a simple non-model approach. To simplify the problem, two time dimensions were eliminated by assuming that the start date is equal to zero for all trades. ${ }^{11}$ Now one can use historical correlations between swap rates of different tenors as proxies for correlations between MTM values of trades with different remaining maturities.

11 Since real IR portfolios are dominated by ongoing IR swaps, this assumption should not lead to large distortions.

Historical correlations between weekly changes of swap rates of different tenors (between one year and 30 years) for each of four major currencies (USD, EUR, GBP and JPY) were calculated for the time period from January 1, 2005 to December 31, 2009. To find a parametric function of two tenors that adequately describes the historical correlations calculated for each currency, a two-step procedure was followed:

- Reducing the two tenor dimensions into a single effective dimension: The data plotted as a function of this effective dimension should lie on a smooth curve rather than be scattered. Data points in Figure 2 show the historical correlations as a function of $\left|M_{i}-M_{k}\right| / \min \left\{M_{i}, M_{k}\right\}$ for the four major currencies, where $M_{i}$ is the tenor of swap rate $i$. One can see that the data points group along smooth lines in all four plots, so this combination of tenors is a good approximation for the effective single dimension.
- $\quad$ Finding a simple parametric fitting function of the effective dimension: The solid curve in each of the panels of Figure 2 represents the function given by

$$
\begin{equation*}
\rho_{i k}=\frac{1}{\left(1+a \frac{\left|M_{i}-M_{k}\right|}{\min \left\{M_{i}, M_{k}\right\}}\right)^{b}} \tag{42}
\end{equation*}
$$

with the following values of the parameters: $(a=0.15 ; b=0.5)$ for USD and ( $a=0.15$; $b=0.7$ ) for EUR, GBP and JPY.

Since values $a=0.15$ and $b=0.7$ used in Equation (42) adequately describe three out of four major currencies, it was decided to apply these values to all currencies.

One could apply Equation (42) directly to calculate correlations between any pair of IR trades of the same hedging set (ie the same currency). However, this approach would involve a double summation across the trades, which could become problematic for large netting sets. To overcome this difficulty, it was decided to create maturity buckets and treat all trades within a given maturity bucket as being driven by a single factor. Under this approach, the double summation only applies to a small fixed number of buckets rather than to a potentially large number of individual trades. The SA-CCR specifies three maturity buckets: (1) 0-1 year (midpoint is 0.5 year); (2) 1-5 years (midpoint is three years); (3) above five years (midpoint is set to 18 years). Applying Equation (42) with parameters $a=0.15$ and $b=0.7$ to the midpoints of these maturity buckets yields the following correlation values: $68 \%$ between buckets 1 and 2[^5]and 2 and 3 and $28 \%$ between buckets 1 and 3 . Rounding these numbers to $70 \%$ and $30 \%$, respectively, results in Equation (29).

Figure 2: Swap rate correlations and the parametric fitting function for G4 currencies

## 6.2 Deltas for CDO

Let us consider a CDO structure of $n$ tranches defined on a credit index. Tranche $i$ is specified by the attachment point $P_{i-1}$ and the detachment point $P_{i}$ (with $P_{0}=0$ and $P_{n}=1$ ). The thickness of tranche $i$ is given by $\delta P_{i}=P_{i}-P_{i-1}$ (where $i=1, \ldots, n$ ). A position in all $n$ tranches of a CDO structure is economically equivalent to a single position in the underlying index. The SA-CCR assumes that an index CDS and any CDO tranche referencing that index are driven by the same factor. Under this assumption, the add-on of a portfolio of long tranche positions (ie bought protection) is equal to the sum of the addons of individual tranches, and the equivalence of the entire CDO capital structure to the underlying index can be expressed via

$$
\begin{equation*}
\sum_{i=1}^{n} \delta\left(P_{i-1}, P_{i}\right) \cdot \delta P_{i}=1 \tag{43}
\end{equation*}
$$

where $\delta(A, D)$ is delta of a long position in a tranche with the attachment point $A$ and the detachment point $D$ with respect to the credit spread of the underlying index.

In the limit $n \rightarrow \infty$, the tranches become infinitesimally thin, and the summation in Equation (43) transforms into an integral:

$$
\begin{equation*}
\int_{0}^{1} g(P) \cdot d P=1 \tag{44}
\end{equation*}
$$

Specifying a suitable function $g(\cdot)$ of a single argument that satisfies Equation (44) would allow one to calculate delta of a tranche as the average of this function between the attachment point $A$ and the detachment point $D$ :

$$
\begin{equation*}
\delta(A, D)=\frac{1}{D-A} \cdot \int_{A}^{D} g(P) \cdot d P \tag{45}
\end{equation*}
$$

Function $g(P)$ can be interpreted as delta of an infinitesimally thin tranche (or, a tranchelet) with the attachment point $P$. Since more senior tranches should have smaller add-ons than more junior tranches, function $g(\cdot)$ should be monotonically decreasing.

It is extremely challenging to derive function $g(\cdot)$ from the fundamentals. Instead, a benchmarking exercise was used to calibrate this function for the SA-CCR. Banks participating in the exercise were asked to calculate EEPE for all tranches referencing the CDX.NA.IG index. Then, the average across banks for each quantity was calculated (the highest and the lowest reported values were excluded from the average) for both current and stressed states of the market. Ratios of the average tranche EEPE to the sum of average EEPE across all tranches are essentially IMM-implied values of tranche delta; they were used for the calibration.

After trying several simple parametric functions, it was found that tranchelet delta given by ${ }^{12}$

$$
\begin{equation*}
g(P)=\frac{1+\lambda}{(1+\lambda P)^{2}} \tag{46}
\end{equation*}
$$

with $\lambda=14$ describes the IMM-implied tranche deltas for CDX.NA.IG reasonably well. Figure 3 shows this function along with the value equal to one for the underlying index. One can see from the plot that tranchelets with the attachment point below (above) the value of about $20.5 \%$ are treated more (less)
conservatively than the index. Delta for any finite tranche can be calculated as the average of the tranchelet delta function between the attachment point $A$ and detachment point $D$. For the function given by Equation (46), this averaging can be performed analytically, resulting in

$$
\begin{equation*}
\delta(A, D)=\frac{1+\lambda}{(1+\lambda A) \cdot(1+\lambda D)} \tag{47}
\end{equation*}
$$

which was chosen (with $\lambda=14$ ) as delta for CDO trades under the SA-CCR.

Figure 3: Delta assumed by the SA-CCR for infinitesimally thin tranches.

## References

Basel Committee on Banking Supervision (1988): International convergence of capital measurement and capital standards, July. $\qquad$
(2006): International convergence of capital measurement and capital standards: A revised framework, June. $\qquad$
(2010): Basel III: A global regulatory framework for more resilient banks and banking systems, December. $\qquad$
(2013): The non-internal model method for capitalising counterparty credit risk, consultative document, June.

Canabarro, E, E Picoult and T Wilde (2003): "Analysing counterparty risk", Risk, September, pp 117-22.

Gibson, M (2005): "Measuring counterparty credit exposure to a margined counterparty" in M Pykhtin (ed), Counterparty credit risk modelling, Risk Books.

Gregory J (2012): Counterparty credit risk and credit value adjustment, Wiley.

ISDA-TBMA-LIBA (2003): Counterparty risk treatment of OTC derivatives and securities financing transactions, June, www.isda.org/c_and_a/pdf/counterpartyrisk.pdf.

Pykhtin, M (2010): "Collateralised credit exposure" in E Canabarro (ed), Counterparty credit risk, Risk Books. $\qquad$
(2011): "Counterparty risk management and valuation" in T Bielecky, D Brigo and F Patras (eds), Credit risk frontiers, Wiley.

- (2014): "The non-internal model method for counterparty credit risk" in E Canabarro and M Pykhtin (eds), Counterparty risk management, Risk Books.

Wilde, T (2005): "Analytic methods for portfolio counterparty risk" in M Pykhtin (ed), Counterparty credit risk modelling, Risk Books.


