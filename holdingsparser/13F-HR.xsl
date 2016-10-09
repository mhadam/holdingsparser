<xsl:stylesheet version="2.0"
  xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
<xsl:output method="text" encoding="UTF-8"/>

<xsl:variable name="newline"><xsl:text>
</xsl:text></xsl:variable>
<xsl:variable name="tab"><xsl:text>&#x09;</xsl:text></xsl:variable>

<xsl:template match="/">
  <xsl:text>Name&#x09;TitleofClass&#x09;Cusip&#x09;Value&#x09;ShrsOrPrnAmt&#x09;SshPrnAmt&#x09;SshPrnType&#x09;InvestmentDiscretion&#x09;VotingAuthoritySole&#x09;VotingAuthorityShared&#x09;VotingAuthorityNone</xsl:text>
  <xsl:value-of select="$newline"/>

  <xsl:for-each select="informationtable/infotable">
    <xsl:value-of select="normalize-space(nameofissuer)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(titleofclass)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(cusip)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(value)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(shrsorprnamt/sshprnamt)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(shrsorprnamt/sshprnamttype)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(investmentdiscretion)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(votingauthority/sole)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(votingauthority/shared)"/><xsl:value-of select="$tab"/>
    <xsl:value-of select="normalize-space(votingauthority/none)"/><xsl:value-of select="$newline"/>
  </xsl:for-each>
</xsl:template>

</xsl:stylesheet>