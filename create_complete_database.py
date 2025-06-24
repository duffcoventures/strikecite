#!/usr/bin/env python3
"""
Create the COMPLETE comprehensive legal reporters database based on the user's full RTF content
This includes ALL federal, state, regional, and specialized court reporters
"""
import json

def create_complete_legal_reporters():
    """
    Complete legal reporters database with all U.S. court reporters
    Based on the comprehensive data provided by the user
    """
    
    legal_reporters = [
        # FEDERAL SUPREME COURT
        {
            "abbreviation": "U.S.",
            "aliases": ["US", "U. S."],
            "description": "United States Reports - official reporter for U.S. Supreme Court decisions. Continuous volume numbering (no series).",
            "court_level": "Supreme Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["USSC (informal shorthand for Supreme Court)", "omitting periods (US for U.S.)"],
            "placeholder_examples": ["410 U.S. 113 (1973)", "576 U.S. 644 (2015)"]
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
        
        # FEDERAL APPELLATE
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
            "abbreviation": "U.S. App. D.C.",
            "aliases": ["App. D.C."],
            "description": "Reports of the D.C. Circuit - official reporter for D.C. Circuit cases (parallel cite with F.2d).",
            "court_level": "Federal Court of Appeals",
            "jurisdiction": "Federal (D.C. Circuit)",
            "states": [],
            "common_citation_mistakes": ["Confusing with local D.C. Court of Appeals"],
            "placeholder_examples": ["123 U.S. App. D.C. 56, 351 F.2d 489 (D.C. Cir. 1965)"]
        },
        
        # FEDERAL DISTRICT
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
            "abbreviation": "F.R.D.",
            "aliases": [],
            "description": "Federal Rules Decisions - district court rulings on procedural issues.",
            "court_level": "Federal District Courts",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["85 F.R.D. 127 (S.D.N.Y. 1980)"]
        },
        
        # FEDERAL SPECIALIZED COURTS
        {
            "abbreviation": "B.R.",
            "aliases": ["Bankr."],
            "description": "Bankruptcy Reporter - U.S. Bankruptcy Court decisions.",
            "court_level": "Federal Bankruptcy Courts",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["50 B.R. 5 (Bankr. N.D. Ill. 1985)"]
        },
        {
            "abbreviation": "Fed. Cl.",
            "aliases": [],
            "description": "Federal Claims Reporter - Court of Federal Claims decisions (1982-present).",
            "court_level": "Federal Claims Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["150 Fed. Cl. 662 (2020)"]
        },
        {
            "abbreviation": "Ct. Cl.",
            "aliases": [],
            "description": "Court of Claims Reports - U.S. Court of Claims official reporter (1855-1982).",
            "court_level": "Federal Claims Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["224 Ct. Cl. 744 (1980)"]
        },
        {
            "abbreviation": "C.C.P.A.",
            "aliases": ["Cust. & Pat. App."],
            "description": "Court of Customs & Patent Appeals Reports (pre-1982).",
            "court_level": "Special Federal Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["496 F.2d 876 (C.C.P.A. 1974)"]
        },
        {
            "abbreviation": "M.J.",
            "aliases": [],
            "description": "Military Justice Reporter - Court of Military Appeals/CAAF cases (1975-present).",
            "court_level": "Military Appeals Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Omitting periods (MJ)"],
            "placeholder_examples": ["80 M.J. 129 (C.A.A.F. 2020)"]
        },
        {
            "abbreviation": "C.M.R.",
            "aliases": [],
            "description": "Court-Martial Reports - military appeals (1951-1975).",
            "court_level": "Military Appeals Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["5 C.M.R. 50 (C.M.A. 1952)"]
        },
        {
            "abbreviation": "C.M.A.",
            "aliases": [],
            "description": "Court of Military Appeals Reports - official reports (1951-1980s).",
            "court_level": "Military Appeals Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["24 C.M.A. 108 (1975)"]
        },
        {
            "abbreviation": "Vet. App.",
            "aliases": [],
            "description": "Veterans Appeals Reporter - U.S. Court of Appeals for Veterans Claims cases.",
            "court_level": "Special Federal Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["30 Vet. App. 54 (2018)"]
        },
        {
            "abbreviation": "Ct. Int'l Trade",
            "aliases": ["C.I.T."],
            "description": "Court of International Trade Reports - official reporter for trade court.",
            "court_level": "Special Federal Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["19 C.I.T. 1 (1995)"]
        },
        {
            "abbreviation": "T.C.",
            "aliases": [],
            "description": "Tax Court Reports - U.S. Tax Court regular opinions.",
            "court_level": "Tax Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["150 T.C. 1 (2018)"]
        },
        {
            "abbreviation": "T.C. Memo",
            "aliases": ["T.C.M."],
            "description": "Tax Court Memorandum Decisions - unofficial numbering of Tax Court memo opinions.",
            "court_level": "Tax Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["T.C. Memo 2020-5"]
        },
        {
            "abbreviation": "B.T.A.",
            "aliases": [],
            "description": "Board of Tax Appeals Reports - predecessor to Tax Court (1924-42).",
            "court_level": "Tax Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["45 B.T.A. 104 (1941)"]
        },
        
        # REGIONAL REPORTERS
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
            "abbreviation": "S.E.3d",
            "aliases": [],
            "description": "South Eastern Reporter, Third Series - emerging third series for SE states.",
            "court_level": "State Appellate Courts",
            "jurisdiction": "Regional",
            "states": ["GA","NC","SC","VA","WV"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["545 S.E.3d 548 (Ga. 2022)"]
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
        },
        
        # MAJOR STATE OFFICIAL REPORTERS
        {
            "abbreviation": "Ala.",
            "aliases": [],
            "description": "Alabama Reports - Alabama Supreme Court official reporter (1840-1976).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Alabama",
            "states": ["Alabama"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["287 Ala. 372 (1971)"]
        },
        {
            "abbreviation": "Ala. App.",
            "aliases": [],
            "description": "Alabama Appellate Reports - Alabama appellate courts (1910-1976).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Alabama",
            "states": ["Alabama"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["45 Ala. App. 233 (1969)"]
        },
        {
            "abbreviation": "Alaska",
            "aliases": [],
            "description": "Alaska Reports - territorial and early statehood reporter (1884-1959).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Alaska",
            "states": ["Alaska"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["12 Alaska 10 (1947)"]
        },
        {
            "abbreviation": "Ariz.",
            "aliases": [],
            "description": "Arizona Reports - Arizona Supreme Court official reporter (1866-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Arizona",
            "states": ["Arizona"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["250 Ariz. 580 (2021)"]
        },
        {
            "abbreviation": "Ariz. App.",
            "aliases": [],
            "description": "Arizona Appeals Reports - Arizona Court of Appeals (1965-1976).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Arizona",
            "states": ["Arizona"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["1 Ariz. App. 1 (1965)"]
        },
        {
            "abbreviation": "Ark.",
            "aliases": [],
            "description": "Arkansas Reports - Arkansas Supreme Court official reporter (1837-2009).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Arkansas",
            "states": ["Arkansas"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["375 Ark. 1 (2008)"]
        },
        {
            "abbreviation": "Ark. App.",
            "aliases": [],
            "description": "Arkansas Appellate Reports - Arkansas Court of Appeals (1981-2009).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Arkansas",
            "states": ["Arkansas"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["60 Ark. App. 198 (1998)"]
        },
        {
            "abbreviation": "Cal.",
            "aliases": [],
            "description": "California Reports - California Supreme Court official reporter (Cal., Cal. 2d, Cal. 3d, Cal. 4th, Cal. 5th).",
            "court_level": "State Supreme Court",
            "jurisdiction": "California",
            "states": ["California"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["5 Cal. 5th 277 (2018)"]
        },
        {
            "abbreviation": "Cal. 2d",
            "aliases": [],
            "description": "California Reports, Second Series (1934-1969).",
            "court_level": "State Supreme Court",
            "jurisdiction": "California",
            "states": ["California"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["33 Cal. 2d 80 (1948)"]
        },
        {
            "abbreviation": "Cal. 3d",
            "aliases": [],
            "description": "California Reports, Third Series (1969-1991).",
            "court_level": "State Supreme Court",
            "jurisdiction": "California",
            "states": ["California"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["13 Cal. 3d 758 (1975)"]
        },
        {
            "abbreviation": "Cal. 4th",
            "aliases": [],
            "description": "California Reports, Fourth Series (1991-2016).",
            "court_level": "State Supreme Court",
            "jurisdiction": "California",
            "states": ["California"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["21 Cal. 4th 543 (1999)"]
        },
        {
            "abbreviation": "Cal. 5th",
            "aliases": [],
            "description": "California Reports, Fifth Series (2016-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "California",
            "states": ["California"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["1 Cal. 5th 230 (2016)"]
        },
        {
            "abbreviation": "Cal. App.",
            "aliases": ["Cal. App. 2d", "Cal. App. 3d", "Cal. App. 4th", "Cal. App. 5th"],
            "description": "California Appellate Reports - California Court of Appeal (1st-5th series).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "California",
            "states": ["California"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["10 Cal. App. 5th 594 (2017)"]
        },
        {
            "abbreviation": "Colo.",
            "aliases": [],
            "description": "Colorado Reports - Colorado Supreme Court official reporter (1864-1980).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Colorado",
            "states": ["Colorado"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["200 Colo. 456 (1980)"]
        },
        {
            "abbreviation": "Colo. App.",
            "aliases": [],
            "description": "Colorado Appellate Reports - Colorado Court of Appeals (sporadic periods).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Colorado",
            "states": ["Colorado"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["34 Colo. App. 268 (1975)"]
        },
        {
            "abbreviation": "Conn.",
            "aliases": [],
            "description": "Connecticut Reports - Connecticut Supreme Court official reporter (1814-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Connecticut",
            "states": ["Connecticut"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["322 Conn. 1 (2016)"]
        },
        {
            "abbreviation": "Conn. App.",
            "aliases": [],
            "description": "Connecticut Appellate Reports - Connecticut Appellate Court (1983-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Connecticut",
            "states": ["Connecticut"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["210 Conn. App. 579 (2022)"]
        },
        {
            "abbreviation": "Conn. Supp.",
            "aliases": [],
            "description": "Connecticut Supplement - selected Superior Court decisions (1935-present).",
            "court_level": "State Trial Court",
            "jurisdiction": "Connecticut",
            "states": ["Connecticut"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["58 Conn. Supp. 152 (2015)"]
        },
        {
            "abbreviation": "Del.",
            "aliases": [],
            "description": "Delaware Reports - Delaware Supreme Court official reporter (1920-1966).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Delaware",
            "states": ["Delaware"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["59 Del. 544 (1966)"]
        },
        {
            "abbreviation": "Del. Ch.",
            "aliases": [],
            "description": "Delaware Chancery Reports - Court of Chancery official reporter (1814-1968).",
            "court_level": "State Chancery Court",
            "jurisdiction": "Delaware",
            "states": ["Delaware"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["30 Del. Ch. 249 (1952)"]
        },
        {
            "abbreviation": "Fla.",
            "aliases": [],
            "description": "Florida Reports - Florida Supreme Court official reporter (1846-1948).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Florida",
            "states": ["Florida"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["160 Fla. 833 (1948)"]
        },
        {
            "abbreviation": "Ga.",
            "aliases": [],
            "description": "Georgia Reports - Georgia Supreme Court official reporter (1846-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Georgia",
            "states": ["Georgia"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["310 Ga. 411 (2020)"]
        },
        {
            "abbreviation": "Ga. App.",
            "aliases": [],
            "description": "Georgia Appeals Reports - Georgia Court of Appeals official reporter (1907-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Georgia",
            "states": ["Georgia"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["356 Ga. App. 160 (2020)"]
        },
        {
            "abbreviation": "Haw.",
            "aliases": [],
            "description": "Hawaii Reports - Hawaii Supreme Court official reporter (1847-1994).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Hawaii",
            "states": ["Hawaii"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["75 Haw. 224 (1993)"]
        },
        {
            "abbreviation": "Idaho",
            "aliases": [],
            "description": "Idaho Reports - Idaho Supreme Court official reporter (1866-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Idaho",
            "states": ["Idaho"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["166 Idaho 280 (2020)"]
        },
        {
            "abbreviation": "Ill.",
            "aliases": [],
            "description": "Illinois Reports - Illinois Supreme Court official reporter (1819-2011).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Illinois",
            "states": ["Illinois"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["238 Ill. 2d 233 (2010)"]
        },
        {
            "abbreviation": "Ill. 2d",
            "aliases": [],
            "description": "Illinois Reports, Second Series (1950s-2011).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Illinois",
            "states": ["Illinois"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["50 Ill. 2d 20 (1971)"]
        },
        {
            "abbreviation": "Ill. App.",
            "aliases": ["Ill. App. 2d", "Ill. App. 3d"],
            "description": "Illinois Appellate Court Reports (1877-2011).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Illinois",
            "states": ["Illinois"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["327 Ill. App. 3d 441 (2001)"]
        },
        {
            "abbreviation": "Ind.",
            "aliases": [],
            "description": "Indiana Reports - Indiana Supreme Court official reporter (1848-1981).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Indiana",
            "states": ["Indiana"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["275 Ind. 30 (1981)"]
        },
        {
            "abbreviation": "Ind. App.",
            "aliases": [],
            "description": "Indiana Appellate Court Reports (1890-1979).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Indiana",
            "states": ["Indiana"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["189 Ind. App. 1 (1979)"]
        },
        {
            "abbreviation": "Iowa",
            "aliases": [],
            "description": "Iowa Reports - Iowa Supreme Court official reporter (1839-1968).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Iowa",
            "states": ["Iowa"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["259 Iowa 813 (1967)"]
        },
        {
            "abbreviation": "Kan.",
            "aliases": [],
            "description": "Kansas Reports - Kansas Supreme Court official reporter (1862-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Kansas",
            "states": ["Kansas"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["312 Kan. 238 (2020)"]
        },
        {
            "abbreviation": "Kan. App. 2d",
            "aliases": [],
            "description": "Kansas Court of Appeals Reports (1977-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Kansas",
            "states": ["Kansas"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["1 Kan. App. 2d 367 (1977)"]
        },
        {
            "abbreviation": "Ky.",
            "aliases": [],
            "description": "Kentucky Reports - Kentucky highest court official reports (1785-1951).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Kentucky",
            "states": ["Kentucky"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["314 Ky. 207 (1951)"]
        },
        {
            "abbreviation": "La.",
            "aliases": [],
            "description": "Louisiana Reports - Louisiana Supreme Court official reporter (1813-1972).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Louisiana",
            "states": ["Louisiana"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["259 La. 23 (1971)"]
        },
        {
            "abbreviation": "Me.",
            "aliases": [],
            "description": "Maine Reports - Maine Supreme Judicial Court official reporter (1820-1965).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Maine",
            "states": ["Maine"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["161 Me. 123 (1965)"]
        },
        {
            "abbreviation": "Md.",
            "aliases": [],
            "description": "Maryland Reports - Maryland Court of Appeals official reporter (1658-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Maryland",
            "states": ["Maryland"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["472 Md. 52 (2021)"]
        },
        {
            "abbreviation": "Md. App.",
            "aliases": [],
            "description": "Maryland Appellate Reports - Maryland Court of Special Appeals (1967-2022).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Maryland",
            "states": ["Maryland"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["250 Md. App. 682 (2021)"]
        },
        {
            "abbreviation": "Mass.",
            "aliases": [],
            "description": "Massachusetts Reports - Massachusetts Supreme Judicial Court official reporter (1804-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Massachusetts",
            "states": ["Massachusetts"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["484 Mass. 279 (2020)"]
        },
        {
            "abbreviation": "Mass. App. Ct.",
            "aliases": [],
            "description": "Massachusetts Appeals Court Reports (1972-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Massachusetts",
            "states": ["Massachusetts"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["99 Mass. App. Ct. 110 (2021)"]
        },
        {
            "abbreviation": "Mich.",
            "aliases": [],
            "description": "Michigan Reports - Michigan Supreme Court official reporter (1840-2016).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Michigan",
            "states": ["Michigan"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["498 Mich. 533 (2016)"]
        },
        {
            "abbreviation": "Mich. App.",
            "aliases": [],
            "description": "Michigan Appeals Reports - Michigan Court of Appeals (1965-2016).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Michigan",
            "states": ["Michigan"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["320 Mich. App. 628 (2017)"]
        },
        {
            "abbreviation": "Minn.",
            "aliases": [],
            "description": "Minnesota Reports - Minnesota Supreme Court official reporter (1851-1977).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Minnesota",
            "states": ["Minnesota"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["300 Minn. 1 (1977)"]
        },
        {
            "abbreviation": "Miss.",
            "aliases": [],
            "description": "Mississippi Reports - Mississippi Supreme Court official reporter (1839-1966).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Mississippi",
            "states": ["Mississippi"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["254 Miss. 47 (1965)"]
        },
        {
            "abbreviation": "Mo.",
            "aliases": [],
            "description": "Missouri Reports - Missouri Supreme Court official reporter (1821-1956).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Missouri",
            "states": ["Missouri"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["364 Mo. 779 (1954)"]
        },
        {
            "abbreviation": "Mo. App.",
            "aliases": [],
            "description": "Missouri Appellate Reports - Missouri Courts of Appeals (late 1800s-1950s).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Missouri",
            "states": ["Missouri"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["233 Mo. App. 173 (1938)"]
        },
        {
            "abbreviation": "Mont.",
            "aliases": [],
            "description": "Montana Reports - Montana Supreme Court official reporter (1868-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Montana",
            "states": ["Montana"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["400 Mont. 1 (2020)"]
        },
        {
            "abbreviation": "Neb.",
            "aliases": [],
            "description": "Nebraska Reports - Nebraska Supreme Court official reporter (1871-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Nebraska",
            "states": ["Nebraska"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["307 Neb. 1 (2020)"]
        },
        {
            "abbreviation": "Neb. App.",
            "aliases": [],
            "description": "Nebraska Appellate Reports - Nebraska Court of Appeals (1995-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Nebraska",
            "states": ["Nebraska"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["28 Neb. App. 908 (2021)"]
        },
        {
            "abbreviation": "Nev.",
            "aliases": [],
            "description": "Nevada Reports - Nevada Supreme Court official reporter (1865-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Nevada",
            "states": ["Nevada"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["138 Nev. 1 (2022)"]
        },
        {
            "abbreviation": "N.H.",
            "aliases": [],
            "description": "New Hampshire Reports - NH Supreme Court official reporter (1816-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "New Hampshire",
            "states": ["New Hampshire"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["173 N.H. 183 (2020)"]
        },
        {
            "abbreviation": "N.J.",
            "aliases": [],
            "description": "New Jersey Reports - NJ Supreme Court official reporter (1948-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "New Jersey",
            "states": ["New Jersey"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["255 N.J. 529 (2023)"]
        },
        {
            "abbreviation": "N.J. Super.",
            "aliases": [],
            "description": "New Jersey Superior Court Reports - Appellate Division and trial decisions (1948-present).",
            "court_level": "State Intermediate Appellate / Trial",
            "jurisdiction": "New Jersey",
            "states": ["New Jersey"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["440 N.J. Super. 400 (App. Div. 2015)"]
        },
        {
            "abbreviation": "N.M.",
            "aliases": [],
            "description": "New Mexico Reports - New Mexico Supreme Court official reporter (1852-2012).",
            "court_level": "State Supreme Court",
            "jurisdiction": "New Mexico",
            "states": ["New Mexico"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["150 N.M. XL (2011)"]
        },
        {
            "abbreviation": "N.M. App.",
            "aliases": [],
            "description": "New Mexico Appellate Reports - NM Court of Appeals (1966-2012).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "New Mexico",
            "states": ["New Mexico"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["150 N.M. App. 1 (2011)"]
        },
        {
            "abbreviation": "N.Y.",
            "aliases": ["N.Y.2d", "N.Y.3d"],
            "description": "New York Reports - NY Court of Appeals official reporter (1847-present, multiple series).",
            "court_level": "State Highest Court (Court of Appeals)",
            "jurisdiction": "New York",
            "states": ["New York"],
            "common_citation_mistakes": ["Using NY instead of N.Y."],
            "placeholder_examples": ["34 N.Y.3d 114 (2019)"]
        },
        {
            "abbreviation": "A.D.",
            "aliases": ["App. Div.", "A.D.2d", "A.D.3d"],
            "description": "Appellate Division Reports - New York Supreme Court Appellate Division (multiple series).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "New York",
            "states": ["New York"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["180 A.D.3d 10 (2020)"]
        },
        {
            "abbreviation": "N.Y.S.",
            "aliases": ["N.Y.S.2d", "N.Y.S.3d"],
            "description": "New York Supplement - West's regional reporter for NY state courts (multiple series).",
            "court_level": "State (all levels)",
            "jurisdiction": "New York",
            "states": ["New York"],
            "common_citation_mistakes": ["Using N.Y.S. cite alone when official cite exists"],
            "placeholder_examples": ["966 N.Y.S.2d 520 (2013)"]
        },
        {
            "abbreviation": "Misc.",
            "aliases": ["Misc. 2d", "Misc. 3d"],
            "description": "Miscellaneous Reports - NY trial court opinions (multiple series).",
            "court_level": "State Trial Courts",
            "jurisdiction": "New York",
            "states": ["New York"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["30 Misc. 3d 1201(A) (2010)"]
        },
        {
            "abbreviation": "N.C.",
            "aliases": [],
            "description": "North Carolina Reports - NC Supreme Court official reporter (1789-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "North Carolina",
            "states": ["North Carolina"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["374 N.C. 516 (2020)"]
        },
        {
            "abbreviation": "N.C. App.",
            "aliases": [],
            "description": "North Carolina Court of Appeals Reports (1968-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "North Carolina",
            "states": ["North Carolina"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["273 N.C. App. 12 (2020)"]
        },
        {
            "abbreviation": "N.D.",
            "aliases": [],
            "description": "North Dakota Reports - ND Supreme Court official reporter (1878-1953).",
            "court_level": "State Supreme Court",
            "jurisdiction": "North Dakota",
            "states": ["North Dakota"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["82 N.D. 578 (1957)"]
        },
        {
            "abbreviation": "Ohio St.",
            "aliases": ["Ohio St. 2d", "Ohio St. 3d"],
            "description": "Ohio State Reports - Ohio Supreme Court official reporter (multiple series).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Ohio",
            "states": ["Ohio"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["65 Ohio St. 3d 545 (1992)"]
        },
        {
            "abbreviation": "Ohio App.",
            "aliases": ["Ohio App. 2d", "Ohio App. 3d"],
            "description": "Ohio Appellate Reports - Ohio Courts of Appeals (multiple series).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Ohio",
            "states": ["Ohio"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["1 Ohio App. 2d 1 (1964)"]
        },
        {
            "abbreviation": "Okla.",
            "aliases": [],
            "description": "Oklahoma Reports - Oklahoma Supreme Court official reporter (1900-1954).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Oklahoma",
            "states": ["Oklahoma"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["91 Okla. 180 (1942)"]
        },
        {
            "abbreviation": "Okla. Crim.",
            "aliases": ["Okl. Cr."],
            "description": "Oklahoma Criminal Reports - Oklahoma Court of Criminal Appeals (1908-1954).",
            "court_level": "State Criminal Appeals",
            "jurisdiction": "Oklahoma",
            "states": ["Oklahoma"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["55 Okl. Cr. 100 (1943)"]
        },
        {
            "abbreviation": "Or.",
            "aliases": [],
            "description": "Oregon Reports - Oregon Supreme Court official reporter (1853-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Oregon",
            "states": ["Oregon"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["368 Or. 1 (2021)"]
        },
        {
            "abbreviation": "Or. App.",
            "aliases": [],
            "description": "Oregon Appellate Reports - Oregon Court of Appeals (1969-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Oregon",
            "states": ["Oregon"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["307 Or. App. 244 (2020)"]
        },
        {
            "abbreviation": "Pa.",
            "aliases": [],
            "description": "Pennsylvania State Reports - Pa. Supreme Court official reporter (1845-1997).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Pennsylvania",
            "states": ["Pennsylvania"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["547 Pa. 321 (1997)"]
        },
        {
            "abbreviation": "Pa. Super.",
            "aliases": [],
            "description": "Pennsylvania Superior Court Reports (1895-1997).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Pennsylvania",
            "states": ["Pennsylvania"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["456 Pa. Super. 123 (1997)"]
        },
        {
            "abbreviation": "Pa. Commw.",
            "aliases": [],
            "description": "Pennsylvania Commonwealth Court Reports (1970-1995).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Pennsylvania",
            "states": ["Pennsylvania"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["168 Pa. Commw. 321 (1994)"]
        },
        {
            "abbreviation": "R.I.",
            "aliases": [],
            "description": "Rhode Island Reports - Rhode Island Supreme Court (1828-1980).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Rhode Island",
            "states": ["Rhode Island"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["120 R.I. 667 (1978)"]
        },
        {
            "abbreviation": "S.C.",
            "aliases": [],
            "description": "South Carolina Reports - S.C. Supreme Court official reporter (1783-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "South Carolina",
            "states": ["South Carolina"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["424 S.C. 579 (2018)"]
        },
        {
            "abbreviation": "S.D.",
            "aliases": [],
            "description": "South Dakota Reports - S.D. Supreme Court official reporter (1879-1996).",
            "court_level": "State Supreme Court",
            "jurisdiction": "South Dakota",
            "states": ["South Dakota"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["527 N.W.2d 394 (S.D. 1995)"]
        },
        {
            "abbreviation": "Tenn.",
            "aliases": [],
            "description": "Tennessee Reports - Tennessee Supreme Court official reporter (1791-1971).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Tennessee",
            "states": ["Tennessee"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["478 S.W.2d 983 (Tenn. 1972)"]
        },
        {
            "abbreviation": "Tex.",
            "aliases": [],
            "description": "Texas Reports - Texas Supreme Court official reporter (1846-1962).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Texas",
            "states": ["Texas"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["162 Tex. 1 (1961)"]
        },
        {
            "abbreviation": "Tex. Crim.",
            "aliases": [],
            "description": "Texas Criminal Reports - Texas Court of Criminal Appeals (1879-1962).",
            "court_level": "State Highest Criminal Court",
            "jurisdiction": "Texas",
            "states": ["Texas"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["160 Tex. Crim. 183 (1953)"]
        },
        {
            "abbreviation": "Utah",
            "aliases": ["Utah 2d"],
            "description": "Utah Reports - Utah Supreme Court official reporter (1851-1999).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Utah",
            "states": ["Utah"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["948 P.2d 712 (Utah 1997)"]
        },
        {
            "abbreviation": "Vt.",
            "aliases": [],
            "description": "Vermont Reports - Vermont Supreme Court official reporter (1829-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Vermont",
            "states": ["Vermont"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["211 Vt. 102 (2020)"]
        },
        {
            "abbreviation": "Va.",
            "aliases": [],
            "description": "Virginia Reports - Virginia Supreme Court official reporter (1790-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Virginia",
            "states": ["Virginia"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["299 Va. 348 (2021)"]
        },
        {
            "abbreviation": "Va. App.",
            "aliases": [],
            "description": "Virginia Court of Appeals Reports (1985-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Virginia",
            "states": ["Virginia"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["72 Va. App. 250 (2020)"]
        },
        {
            "abbreviation": "Wash.",
            "aliases": ["Wash. 2d"],
            "description": "Washington Reports - Washington Supreme Court official reporter (1854-present, 2d series from 1939).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Washington",
            "states": ["Washington"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["200 Wash. 2d 1 (2022)"]
        },
        {
            "abbreviation": "Wash. App.",
            "aliases": ["Wn. App."],
            "description": "Washington Appellate Reports - Washington Court of Appeals (1969-present).",
            "court_level": "State Intermediate Appellate",
            "jurisdiction": "Washington",
            "states": ["Washington"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["12 Wn. App. 2d 783 (2020)"]
        },
        {
            "abbreviation": "W. Va.",
            "aliases": [],
            "description": "West Virginia Reports - W.Va. Supreme Court of Appeals (1864-present).",
            "court_level": "State Supreme Court",
            "jurisdiction": "West Virginia",
            "states": ["West Virginia"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["242 W. Va. 277 (2019)"]
        },
        {
            "abbreviation": "Wis.",
            "aliases": ["Wis. 2d"],
            "description": "Wisconsin Reports - Wis. Supreme Court official reporter (1853-present, 2d series from 1953).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Wisconsin",
            "states": ["Wisconsin"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["244 Wis. 2d 481 (2001)"]
        },
        {
            "abbreviation": "Wyo.",
            "aliases": [],
            "description": "Wyoming Reports - Wyoming Supreme Court official reporter (1869-1954).",
            "court_level": "State Supreme Court",
            "jurisdiction": "Wyoming",
            "states": ["Wyoming"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["70 Wyo. 393 (1954)"]
        },
        
        # NEUTRAL CITATIONS
        {
            "abbreviation": "AR",
            "aliases": [],
            "description": "Arkansas public-domain citation - since 2009, format: Year Ark ### (Supreme) or Year Ark. App ###.",
            "court_level": "State (Neutral)",
            "jurisdiction": "Arkansas",
            "states": ["Arkansas"],
            "common_citation_mistakes": ["Using Ark. instead of Ark (neutral citations omit period)"],
            "placeholder_examples": ["2018 Ark 5", "2018 Ark. App. 12"]
        },
        {
            "abbreviation": "CO",
            "aliases": ["Colo. (neutral)"],
            "description": "Colorado neutral citation - since 2012, format: Year CO ## (Supreme) or Year COA ## (Appeals).",
            "court_level": "State (Neutral)",
            "jurisdiction": "Colorado",
            "states": ["Colorado"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2012 CO 22", "2012 COA 35"]
        },
        {
            "abbreviation": "IL",
            "aliases": [],
            "description": "Illinois neutral citation - since 2011, format: Year IL ### (Supreme) or Year IL App (Dist) ###.",
            "court_level": "State (Neutral)",
            "jurisdiction": "Illinois",
            "states": ["Illinois"],
            "common_citation_mistakes": ["Using Ill. instead of IL in neutral cite"],
            "placeholder_examples": ["2023 IL 123", "2023 IL App (1st) 230123"]
        },
        {
            "abbreviation": "LA",
            "aliases": [],
            "description": "Louisiana neutral docket-based citation - adopted 1994 (e.g., 1998-1234 (La.) format).",
            "court_level": "State (Neutral)",
            "jurisdiction": "Louisiana",
            "states": ["Louisiana"],
            "common_citation_mistakes": ["Using La. official reporter (obsolete after 1972)"],
            "placeholder_examples": ["2003-CC-1234 (La. 2003)"]
        },
        {
            "abbreviation": "MT",
            "aliases": [],
            "description": "Montana neutral citation - since 1998, format: Year MT ##.",
            "court_level": "State (Neutral)",
            "jurisdiction": "Montana",
            "states": ["Montana"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2020 MT 5"]
        },
        {
            "abbreviation": "ND",
            "aliases": [],
            "description": "North Dakota neutral citation - since 1997, format: Year ND ##.",
            "court_level": "State (Neutral)",
            "jurisdiction": "North Dakota",
            "states": ["North Dakota"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2003 ND 140"]
        },
        {
            "abbreviation": "NM",
            "aliases": [],
            "description": "New Mexico neutral citation - since 1997, format: Year-NMSC-## (Supreme) or Year-NMCA-## (Appeals).",
            "court_level": "State (Neutral)",
            "jurisdiction": "New Mexico",
            "states": ["New Mexico"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2015-NMSC-010", "2015-NMCA-012"]
        },
        {
            "abbreviation": "OK",
            "aliases": [],
            "description": "Oklahoma neutral citation - since 1997, format: Year OK ## (Supreme), Year OK CR ## (Criminal), Year OK CIV APP ##.",
            "court_level": "State (Neutral)",
            "jurisdiction": "Oklahoma",
            "states": ["Oklahoma"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2019 OK 5", "2019 OK CR 3"]
        },
        {
            "abbreviation": "SD",
            "aliases": [],
            "description": "South Dakota neutral citation - since 1996, format: Year SD ##.",
            "court_level": "State (Neutral)",
            "jurisdiction": "South Dakota",
            "states": ["South Dakota"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2004 SD 2"]
        },
        {
            "abbreviation": "UT",
            "aliases": [],
            "description": "Utah neutral citation - since 1999, format: Year UT ## (Supreme) or Year UT App ## (Appeals).",
            "court_level": "State (Neutral)",
            "jurisdiction": "Utah",
            "states": ["Utah"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2012 UT 25", "2012 UT App 15"]
        },
        {
            "abbreviation": "WI",
            "aliases": [],
            "description": "Wisconsin neutral citation - since 2000, format: Year WI ## (Supreme) or Year WI App ## (Appeals).",
            "court_level": "State (Neutral)",
            "jurisdiction": "Wisconsin",
            "states": ["Wisconsin"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2010 WI 5", "2010 WI App 20"]
        },
        {
            "abbreviation": "WY",
            "aliases": [],
            "description": "Wyoming neutral citation - since ~2000, format: Year WY ##.",
            "court_level": "State (Neutral)",
            "jurisdiction": "Wyoming",
            "states": ["Wyoming"],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2014 WY 20"]
        },
        
        # VENDOR CITATIONS
        {
            "abbreviation": "WL",
            "aliases": [],
            "description": "Westlaw citation - citation to unpublished cases in Westlaw, format: Year WL ######.",
            "court_level": "Unpublished/Vendor",
            "jurisdiction": "All",
            "states": [],
            "common_citation_mistakes": ["Missing space (2023WL123456 instead of 2023 WL 123456)"],
            "placeholder_examples": ["2023 WL 123456"]
        },
        {
            "abbreviation": "LEXIS",
            "aliases": [],
            "description": "Lexis citation - citation to unpublished cases in Lexis, format often: Year U.S. Dist. LEXIS ##### or similar.",
            "court_level": "Unpublished/Vendor",
            "jurisdiction": "All",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["2023 U.S. Dist. LEXIS 10000"]
        },
        
        # MISCELLANEOUS
        {
            "abbreviation": "slip op.",
            "aliases": [],
            "description": "Slip Opinion - used to cite an opinion not in a reporter (often with a docket or slip op. notation).",
            "court_level": "Unpublished",
            "jurisdiction": "All",
            "states": [],
            "common_citation_mistakes": [],
            "placeholder_examples": ["No. 21-123, slip op. at 5 (Jan. 1, 2023)"]
        },
        {
            "abbreviation": "SCOTUS",
            "aliases": [],
            "description": "Supreme Court of the United States - colloquial acronym, not used in formal citations.",
            "court_level": "Supreme Court",
            "jurisdiction": "Federal",
            "states": [],
            "common_citation_mistakes": ["Using SCOTUS instead of proper reporter or court name"],
            "placeholder_examples": ["SCOTUS decision (2021)"]
        }
    ]
    
    return legal_reporters

if __name__ == "__main__":
    reporters = create_complete_legal_reporters()
    
    # Save the comprehensive legal reporters database
    with open('/app/legal_reporters_comprehensive.json', 'w') as f:
        json.dump(reporters, f, indent=2)
    
    print(f"✅ Created COMPLETE comprehensive legal reporters database with {len(reporters)} entries")
    print("\nBreakdown:")
    
    # Count by jurisdiction
    federal = len([r for r in reporters if r['jurisdiction'] == 'Federal'])
    regional = len([r for r in reporters if r['jurisdiction'] == 'Regional'])
    state_specific = len([r for r in reporters if r['jurisdiction'] not in ['Federal', 'Regional', 'All']])
    
    print(f"Federal reporters: {federal}")
    print(f"Regional reporters: {regional}")  
    print(f"State-specific reporters: {state_specific}")
    print(f"Other (neutral, vendor, etc.): {len(reporters) - federal - regional - state_specific}")
    print("Saved to: /app/legal_reporters_comprehensive.json")