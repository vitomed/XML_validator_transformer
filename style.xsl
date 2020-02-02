<?xml version="1.0"?>
<xsl:stylesheet version="1.0"
 xmlns:xsl="http://www.w3.org/1999/XSL/Transform">
	<xsl:strip-space elements="*"/>
	<xsl:output method="xml" indent="yes"/>
	<xsl:template match="/">
		<xsl:apply-templates/>
	</xsl:template>
	<xsl:template match="PLANETS">
		<xsl:copy>
			<xsl:apply-templates/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="PLANET">
		<xsl:copy>
			<xsl:apply-templates/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="NAME">
		<xsl:copy>
			<xsl:apply-templates/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="MASS">
		<xsl:copy>
			<xsl:value-of select="."/>
			<xsl:value-of select="@UNITS"/>
		</xsl:copy>
	</xsl:template>
	<xsl:template match="DATE"> </xsl:template>
	<xsl:template match="RADIUS"> </xsl:template>
</xsl:stylesheet>
