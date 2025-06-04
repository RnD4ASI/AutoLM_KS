## Scope

56.1 This chapter specifies the treatment of certain non-centrally cleared securities financing transactions (SFTs) with certain counterparties. The requirements are not applicable to banks in jurisdictions that are prohibited from conducting such transactions below the minimum haircut floors specified in CRE56.6 below.

56.2 The haircut floors found in CRE56.6 below apply to the following transactions:

(1) Non-centrally cleared SFTs in which the financing (ie the lending of cash) against collateral other than government securities is provided to counterparties who are not supervised by a regulator that imposes prudential requirements consistent with international norms.

(2) Collateral upgrade transactions with these same counterparties. A collateral upgrade transaction is when a bank lends a security to its counterparty and the counterparty pledges a lower-quality security as collateral, thus allowing the counterparty to exchange a lower-quality security for a higher quality security. For these transactions, the floors must be calculated according to the formula set out in CRE56.9 below.

56.3 SFTs with central banks are not subject to the haircut floors.

56.4 Cash-collateralised securities lending transactions are exempted from the haircut floors where:

(1) Securities are lent (to the bank) at long maturities and the lender of securities reinvests or employs the cash at the same or shorter maturity, therefore not giving rise to material maturity or liquidity mismatch.

(2) Securities are lent (to the bank) at call or at short maturities, giving rise to liquidity risk, only if the lender of the securities reinvests the cash collateral into a reinvestment fund or account subject to regulations or regulatory guidance meeting the minimum standards for reinvestment of cash collateral by securities lenders set out in Section 3.1 of the Policy Framework for Addressing Shadow Banking Risks in Securities Lending and Repos. ${ }^{1}$ For this purpose, banks may rely on representations by securities lenders that their reinvestment of cash collateral meets the minimum standards.

Footnotes

1 Financial Stability Board, Strengthening oversight and regulation of shadow banking, Policy framework for addressing shadow banking risks in securities lending and repos, 29 August 2013, www.fsb.org/wp-content/uploads/r_130829b.pdf.

56.5 Banks that borrow (or lend) securities are exempted from the haircut floors on collateral upgrade transactions if the recipient of the securities that the bank has delivered as collateral (or lent) is either: (i) unable to re-use the securities (for example, because the securities have been provided under a pledge arrangement); or (ii) provides representations to the bank that they do not and will not re-use the securities.

## Haircut floors

56.6 These are the haircut floors for SFTs referred to above (herein referred to as "in-scope SFTs"), expressed as percentages:

| Residual maturity of collateral | Haircut level |  |
| :--- | :--- | :--- |
|  | Corporate and other issuers | Securitised products |
| $\leq 1$ year debt securities, and floating rate notes | $0.5 \%$ | $1 \%$ |


| $>1$ year, $\leq 5$ years debt securities | $1.5 \%$ | $4 \%$ |
| :--- | :--- | :--- |
| $>5$ years, $\leq 10$ years debt securities | $3 \%$ | $6 \%$ |
| $>10$ years debt securities | $4 \%$ | $7 \%$ |
| Main index equities | $6 \%$ |  |
| Other assets within the scope of the framework | $10 \%$ |  |

56.7 In-scope SFTs which do not meet the haircut floors must be treated as unsecured loans to the counterparties.

56.8 To determine whether the treatment in CRE56.7 applies to an in-scope SFT (or a netting set of SFTs in the case of portfolio-level haircuts), we must compare the collateral haircut $\mathrm{H}$ (real or calculated as per the rules below) and a haircut floor $f$ (from CRE56.6 above or calculated as per the below rules).

## Single in-scope SFTs

56.9 For a single in-scope SFT not included in a netting set, the values of $\mathrm{H}$ and $\mathrm{f}$ are computed as:

(1) For a single cash-lent-for-collateral SFT, $\mathrm{H}$ and $\mathrm{f}$ are known since $\mathrm{H}$ is simply defined by the amount of collateral received and $f$ is given in CRE56.6. ${ }^{2}$ For the purposes of this calculation, collateral that is called by either counterparty can be treated collateral received from the moment that it is called (ie the treatment is independent of the settlement period).

(2) For a single collateral-for-collateral SFT, lending collateral A and receiving collateral B, the $\mathrm{H}$ is still be defined by the amount of collateral received but the effective floor of the transaction must integrate the floor of the two types of collateral and can be computed using the following formula, which will be compared to the effective haircut of the transaction, ie (CB/CA)-1: ${ }^{3}$

$f=\left[\left(\frac{1}{1+f_{A}}\right) /\left(\frac{1}{1+f_{B}}\right)\right]-1=\frac{1+f_{B}}{1+f_{A}}-1$

Footnotes 
2 For example, consider an in-scope SFT where 100 cash is lent against 101 of a corporate debt security with a 12-year maturity, $H$ is 1\% [(101-100)/100] and $f$ is $4 \%$ (per CRE56.6). Therefore, the SFT in question would be subject to the treatment in CRE56.7.
3 For example, consider an in-scope SFT where 102 of a corporate debt security with a 10-year maturity is exchanged against 104 of equity, the effective haircut $H$ of the transaction is $104 / 102-1=1.96 \%$ which has to be compared with the effective floor $f$ of 1.06/1.03 - $1=2.91 \%$. Therefore, the SFT in question would be subject to the treatment in CRE56.7.

## Netting set of SFTs

56.10 For a netting set of SFTs an effective "portfolio" floor of the transaction must be computed using the following formula, ${ }^{4}$ where:

(1) Es is the net position in each security (or cash) $s$ that is net lent;

(2) Ct the net position that is net borrowed; and

(3) fs and ft are the haircut floors for the securities that are net lent and net borrowed respectively.

$f_{\text {Portfolio }}=\left[\left(\frac{\sum_{s}\left(\frac{E_{s}}{1+f_{s}}\right)}{\sum_{s} E_{s}}\right) /\left(\frac{\sum_{t}\left(\frac{C_{t}}{1+f_{t}}\right)}{\sum_{t} C_{t}}\right)\right]-1$

Footnotes
4 The formula calculates a weighted average floor of the portfolio.

56.11 For a netting of SFTs, the portfolio does not breach the floor where:

$\frac{\sum C_{c}-\sum E_{s}}{\sum E_{s}} \geq f_{\text {Porftholo }}$

56.12 If the portfolio haircut does breach the floor, then the netting set of SFTs is subject to the treatment in CRE56.7. This treatment should be applied to all trades for which the security received appears in the table in CRE56.6 and for which, within the netting set, the bank is also a net receiver in that security. For the purposes of this calculation, collateral that is called by either counterparty can be treated collateral received from the moment that it is called (ie the treatment is independent of the settlement period).

56.13 The following portfolio of trades gives an example of how this methodology works (it shows a portfolio that does not breach the floor):

| Actual trades | Cash | Sovereign debt | Collateral A | Collateral B |
| :---: | :---: | :---: | :---: | :---: |
| Floor $\left(f_{s}\right)$ | $0 \%$ | $0 \%$ | $6 \%$ | $10 \%$ |
| Portfolio of trades | 50 | 100 | -400 | 250 |
| $\mathrm{E}_{\mathrm{s}}$ | 50 | 100 | 0 | 250 |
| $c_{t}$ | 0 | 0 | 400 | 0 |
| $f_{\text {Pxompolo }}$ | -0.00023 |  |  |  |
| $\frac{\sum C_{t}-\sum E_{s}}{\sum E_{s}}$ | 0 |  |  |  |

$f_{\text {Portfolo }}$

$$
\frac{\sum C_{t}-\sum E_{s}}{\sum E_{s}}
$$

