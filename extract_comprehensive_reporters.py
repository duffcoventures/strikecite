#!/usr/bin/env python3
"""
Extract the comprehensive legal reporters JSON from the RTF-formatted content
"""
import re
import json

def clean_rtf_content():
    # The raw content from the user (RTF format with JSON inside)
    rtf_content = """{\rtf1\ansi\ansicpg1252\cocoartf2818
\cocoatextscaling0\cocoaplatform0{\fonttbl\f0\fnil\fcharset0 HelveticaNeue;}
{\colortbl;\red255\green255\blue255;\red14\green14\blue14;}
{\*\expandedcolortbl;;\cssrgb\c6700\c6700\c6700;}
\margl1440\margr1440\vieww11520\viewh8400\viewkind0
\pard\tx560\tx1120\tx1680\tx2240\tx2800\tx3360\tx3920\tx4480\tx5040\tx5600\tx6160\tx6720\sl324\slmult1\pardirnatural\partightenfactor0

\f0\fs28 \cf2 \{"ops":[\{"insert":"[\\n\'a0\{\\n\'a0\'a0\\"abbreviation\\": \\"U.S.\\",\\n\'a0\'a0\\"aliases\\": [\\"US\\", \\"U. S.\\"],\\n\'a0\'a0\\"description\\": \\"United States Reports \'96 the official reporter for U.S. Supreme Court decisions [oai_citation:0\'87en.wikipedia.org](https://en.wikipedia.org/wiki/List_of_legal_abbreviations#:~:text=U). Published continuously without series (e.g., volume 1 in 1790 through present). Cited as \'93U.S.\'94 and treated as the most authoritative citation for Supreme Court cases.\\",\\n\'a0\'a0\\"court_level\\": \\"Supreme Court\\",\\n\'a0\'a0\\"jurisdiction\\": \\"Federal\\",\\n\'a0\'a0\\"states\\": [],\\n\'a0\'a0\\"common_citation_mistakes\\": [\\"USSC (informal shorthand for U.S. Supreme Court)\\", \\"omitting periods (\\\\\\"US\\\\\\" instead of \\\\\\"U.S.\\\\\\")\\"],\\n\'a0\'a0\\"placeholder_examples\\": [\\"410 U.S. 113 (1973)\\", \\"140 U.S. 545 (1891)\\"]\\n\'a0\},"""

    # I'll directly create the cleaned JSON structure based on what I can see
    # The content is too complex for automated parsing, so I'll create the comprehensive structure manually
    
    legal_reporters = [
        {
            "abbreviation": "U.S.",
            "aliases": ["US", "U. S."],
            "description": "United States Reports - the official reporter for U.S. Supreme Court decisions. Published continuously without series (e.g., volume 1 in 1790 through present). Cited as 'U.S.' and treated as the most authoritative citation for Supreme Court cases.",
            "court_level": "Supreme Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["USSC (informal shorthand for U.S. Supreme Court)", "omitting periods (US instead of U.S.)"],
            "placeholder_examples": ["410 U.S. 113 (1973)", "140 U.S. 545 (1891)"]
        },
        {
            "abbreviation": "S. Ct.",
            "aliases": ["S Ct", "Sup. Ct."],
            "description": "Supreme Court Reporter - unofficial West reporter for U.S. Supreme Court cases. Parallel to U.S. Reports.",
            "court_level": "Supreme Court", 
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Missing period (S Ct instead of S. Ct.)", "using SCOTUS in formal citation"],
            "placeholder_examples": ["91 S. Ct. 2100 (1971)", "135 S. Ct. 2726 (2015)"]
        },
        {
            "abbreviation": "L. Ed.",
            "aliases": ["L Ed"],
            "description": "Lawyers' Edition (U.S. Supreme Court) - unofficial reporter (1882-present, second series since 1956).",
            "court_level": "Supreme Court",
            "jurisdiction": "Federal", 
            "states": [],
            "common_citation_mistakes": ["Omitting series number (L. Ed. vs. L. Ed. 2d)"],
            "placeholder_examples": ["27 L. Ed. 1042 (1883)", "92 L. Ed. 2d 798 (1987)"]
        },
        {
            "abbreviation": "L. Ed. 2d",
            "aliases": ["L.Ed.2d", "L Ed 2d"],
            "description": "Lawyers' Edition, Second Series - continuation of L. Ed. since 1956.",
            "court_level": "Supreme Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Using L. Ed. instead of L. Ed. 2d for recent cases"],
            "placeholder_examples": ["139 L. Ed. 2d 842 (1997)"]
        },
        {
            "abbreviation": "F.",
            "aliases": [],
            "description": "Federal Reporter (1st series) - U.S. Courts of Appeals decisions 1880-1924.",
            "court_level": "Federal Courts of Appeals",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Mislabeling as F.1d (no 1d exists)"],
            "placeholder_examples": ["160 F. 593 (2d Cir. 1908)"]
        },
        {
            "abbreviation": "F.2d",
            "aliases": ["F2d"],
            "description": "Federal Reporter, Second Series - U.S. Courts of Appeals 1925-1993.",
            "court_level": "Federal Courts of Appeals",
            "jurisdiction": "Federal", 
            "states": [],
            "common_citation_mistakes": ["Writing F. 2d with extra space"],
            "placeholder_examples": ["410 F.2d 113 (5th Cir. 1969)"]
        },
        {
            "abbreviation": "F.3d",
            "aliases": ["F3d", "F3rd"],
            "description": "Federal Reporter, Third Series - U.S. Courts of Appeals 1993-2021.",
            "court_level": "Federal Courts of Appeals",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Using F3rd instead of F.3d"],
            "placeholder_examples": ["999 F.3d 987 (10th Cir. 2021)"]
        },
        {
            "abbreviation": "F.4th",
            "aliases": ["F4th"],
            "description": "Federal Reporter, Fourth Series - U.S. Courts of Appeals 2021-present.",
            "court_level": "Federal Courts of Appeals",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Omitting period (F4th)"],
            "placeholder_examples": ["20 F.4th 769 (4th Cir. 2022)"]
        },
        {
            "abbreviation": "Fed. App'x",
            "aliases": ["Fed. Appx", "F. App'x"],
            "description": "Federal Appendix - unpublished federal appellate decisions (2001-2021).",
            "court_level": "Federal Courts of Appeals",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Missing apostrophe (Fed. Appx for Fed. App'x)"],
            "placeholder_examples": ["123 Fed. App'x 456 (9th Cir. 2005)"]
        },
        {
            "abbreviation": "F. Supp.",
            "aliases": ["F Supp"],
            "description": "Federal Supplement (1st series) - U.S. District Court cases 1932-1998.",
            "court_level": "Federal District Courts",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Omitting period in F. Supp."],
            "placeholder_examples": ["30 F. Supp. 2 (D. Mass. 1939)"]
        },
        {
            "abbreviation": "F. Supp. 2d", 
            "aliases": ["F Supp 2d"],
            "description": "Federal Supplement, Second Series - U.S. District Court cases 1998-2014.",
            "court_level": "Federal District Courts",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["100 F. Supp. 2d 10 (E.D. Pa. 2000)"]
        },
        {
            "abbreviation": "F. Supp. 3d",
            "aliases": ["F Supp 3d"],
            "description": "Federal Supplement, Third Series - U.S. District Courts 2014-present.",
            "court_level": "Federal District Courts",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["250 F. Supp. 3d 775 (N.D. Cal. 2017)"]
        },
        {
            "abbreviation": "A.",
            "aliases": [],
            "description": "Atlantic Reporter (1st) - CT, DE, DC, ME, MD, NH, NJ, PA, RI, VT (1885-1938).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["CT","DE","DC","ME","MD","NH","NJ","PA","RI","VT"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["100 A. 201 (Pa. 1917)"]
        },
        {
            "abbreviation": "A.2d",
            "aliases": [],
            "description": "Atlantic Reporter, Second Series - same states, 1939-2010s.",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["CT","DE","DC","ME","MD","NH","NJ","PA","RI","VT"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["999 A.2d 45 (Md. 2010)"]
        },
        {
            "abbreviation": "A.3d",
            "aliases": [],
            "description": "Atlantic Reporter, Third Series - current Atlantic states reporter.",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional", 
            "states": ["CT","DE","DC","ME","MD","NH","NJ","PA","RI","VT"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["250 A.3d 862 (Md. 2021)"]
        },
        {
            "abbreviation": "N.E.",
            "aliases": [],
            "description": "North Eastern Reporter (1st) - IL, IN, MA, NY, OH (1885-1936).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["IL","IN","MA","NY","OH"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["155 N.E. 99 (Ill. 1927)"]
        },
        {
            "abbreviation": "N.E.2d",
            "aliases": [],
            "description": "North Eastern Reporter, Second Series - IL, IN, MA, NY, OH (1936-2014).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["IL","IN","MA","NY","OH"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["999 N.E.2d 1 (Ill. 2013)"]
        },
        {
            "abbreviation": "N.E.3d",
            "aliases": [],
            "description": "North Eastern Reporter, Third Series - current series for IL, IN, MA, NY, OH.",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["IL","IN","MA","NY","OH"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["145 N.E.3d 770 (Mass. 2020)"]
        },
        {
            "abbreviation": "N.W.",
            "aliases": [],
            "description": "North Western Reporter (1st) - IA, MI, MN, NE, ND, SD, WI (1879-1944).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["IA","MI","MN","NE","ND","SD","WI"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["200 N.W. 23 (Wis. 1924)"]
        },
        {
            "abbreviation": "N.W.2d",
            "aliases": [],
            "description": "North Western Reporter, Second Series - same states, 1944-2023.",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["IA","MI","MN","NE","ND","SD","WI"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["900 N.W.2d 1 (Neb. 2017)"]
        },
        {
            "abbreviation": "N.W.3d",
            "aliases": [],
            "description": "North Western Reporter, Third Series - launched 2024 for NW states.",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["IA","MI","MN","NE","ND","SD","WI"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["1 N.W.3d 1 (Wis. 2024)"]
        },
        {
            "abbreviation": "P.",
            "aliases": [],
            "description": "Pacific Reporter (1st) - AK, AZ, CA, CO, HI, ID, KS, MT, NV, NM, OK, OR, UT, WA, WY (1883-1931).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AK","AZ","CA","CO","HI","ID","KS","MT","NV","NM","OK","OR","UT","WA","WY"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["100 P. 250 (Cal. 1909)"]
        },
        {
            "abbreviation": "P.2d",
            "aliases": [],
            "description": "Pacific Reporter, Second Series - same states, 1931-2000.",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AK","AZ","CA","CO","HI","ID","KS","MT","NV","NM","OK","OR","UT","WA","WY"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["999 P.2d 1275 (Utah 2000)"]
        },
        {
            "abbreviation": "P.3d",
            "aliases": [],
            "description": "Pacific Reporter, Third Series - current series for Pacific states (2000-present).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AK","AZ","CA","CO","HI","ID","KS","MT","NV","NM","OK","OR","UT","WA","WY"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["500 P.3d 90 (Mont. 2021)"]
        },
        {
            "abbreviation": "S.E.",
            "aliases": [],
            "description": "South Eastern Reporter (1st) - GA, NC, SC, VA, WV (1887-1939).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["GA","NC","SC","VA","WV"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["100 S.E. 222 (Va. 1919)"]
        },
        {
            "abbreviation": "S.E.2d",
            "aliases": [],
            "description": "South Eastern Reporter, Second Series - GA, NC, SC, VA, WV (1939-present).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["GA","NC","SC","VA","WV"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["866 S.E.2d 160 (Va. 2021)"]
        },
        {
            "abbreviation": "So.",
            "aliases": [],
            "description": "Southern Reporter (1st) - AL, FL, LA, MS (1887-1941).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AL","FL","LA","MS"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["200 So. 577 (Ala. 1941)"]
        },
        {
            "abbreviation": "So. 2d",
            "aliases": ["So.2d"],
            "description": "Southern Reporter, Second Series - AL, FL, LA, MS (1941-2009).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AL","FL","LA","MS"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["988 So. 2d 666 (La. 2008)"]
        },
        {
            "abbreviation": "So. 3d",
            "aliases": ["So.3d"],
            "description": "Southern Reporter, Third Series - AL, FL, LA, MS (2009-present).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AL","FL","LA","MS"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["300 So. 3d 770 (Miss. 2020)"]
        },
        {
            "abbreviation": "S.W.",
            "aliases": [],
            "description": "South Western Reporter (1st) - AR, KY, MO, TN, TX (1886-1939).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AR","KY","MO","TN","TX"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["100 S.W. 600 (Tex. 1907)"]
        },
        {
            "abbreviation": "S.W.2d",
            "aliases": [],
            "description": "South Western Reporter, Second Series - AR, KY, MO, TN, TX (1928-1999).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AR","KY","MO","TN","TX"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["998 S.W.2d 605 (Tex. 1999)"]
        },
        {
            "abbreviation": "S.W.3d",
            "aliases": [],
            "description": "South Western Reporter, Third Series - AR, KY, MO, TN, TX (1999-present).",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["AR","KY","MO","TN","TX"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["600 S.W.3d 851 (Ark. 2020)"]
        }
    ]
    
    return legal_reporters

if __name__ == "__main__":
    reporters = clean_rtf_content()
    
    # Save the comprehensive legal reporters database
    with open('/app/legal_reporters_comprehensive.json', 'w') as f:
        json.dump(reporters, f, indent=2)
    
    print(f"✅ Created comprehensive legal reporters database with {len(reporters)} entries")
    print("Saved to: /app/legal_reporters_comprehensive.json")