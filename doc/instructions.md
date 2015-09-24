Dear Andrea and Christophe,


I spent some time today with the Portuguese UDC data files. I think what we need to do is quite simple, at least at first.


Aida wants our team to replicate what we did with OCLC and Leuven, using the three Portugese data files.


Then she wanted me to replicate my statistical correlation study with them as well. So that one is my kettle of fish, but the first looks quite simple to me. At least if you can do this we can analyze it, compare it to OCLC and Leuven, and have a basic paper from which we can look into specific areas of divergence we notice.


My instructions are below. If you have specific questions let me know. I can Skype with the both of you if that would help.


Won't see you this month but will perhaps visit in August (I know, everybody goes on holiday, but I have a conference in Copenhagen, just nearby).




Forgive the uppercase I was making notes in NOTEPAD:


BNP (Catalog of the BNP?
PORBASE (union catalog of Portuguese libraries)
BNP dominio publico (National Digital Library)



bnd_publico.html

UNIMARC records

extract for each:

identifier
UDC number (field 100)
date of publication (field 210, subfield d)

THE FIRST RECORD DOES NOT HAVE A UDC NUMBER (675) SO WE SKIP IT, OR RECORD THE IDENTIFIER AND A NULL VALUE FOR UDC

<identifier>oai:oai.bn.pt:bndlivre/bnp460850</identifier>
675 NULL
<mx:datafield tag="210" ind1=" " ind2=" "><mx:subfield code="d">[ca 1530-1535]</mx:subfield></mx:datafield>

<identifier>oai:oai.bn.pt:bndlivre/bnp1673462</identifier>
<mx:datafield tag="210" ind1=" " ind2=" "><mx:subfield code="d">[ca 1765]</mx:subfield></mx:datafield>
<mx:datafield tag="675" ind1=" " ind2=" "><mx:subfield code="a">741(=1:469)"17"(084.11)</mx:subfield><mx:subfield code="v">BN</mx:subfield><mx:subfield code="z">por</mx:subfield><mx:subfield code="3">1249346</mx:subfield></mx:datafield>


catalogo_bnp.xml

UNIMARC records

extract for each:

identifier
UDC number (field 100)
date of publication (field 210, subfield d)

<identifier>oai:oai.bn.pt:catalogo/1301</identifier>
<mx:datafield tag="675" ind1=" " ind2=" "><mx:subfield code="a">550</mx:subfield><mx:subfield code="v">med</mx:subfield><mx:subfield code="z">por</mx:subfield><mx:subfield code="3">288201</mx:subfield></mx:datafield>
<mx:datafield tag="210" ind1=" " ind2=" "><mx:subfield code="d">1979</mx:subfield></mx:datafield>


porbase.xml

UNIMARC records

extract for each:

identifier
UDC number (field 675)
date of publication (field 210, subfield d)

<identifier>oai:oai.bn.pt:porbase/59294</identifier>
<mx:datafield tag="675" ind1=" " ind2=" "><mx:subfield code="a">38</mx:subfield><mx:subfield code="v">med</mx:subfield><mx:subfield code="z">por</mx:subfield><mx:subfield code="3">288295</mx:subfield></mx:datafield>
<mx:datafield tag="210" ind1=" " ind2=" "><mx:subfield code="d">1957</mx:subfield></mx:datafield>


IN THE THREE EXAMPLES ABOVE I RECORDED THE ENTIRE FIELD 675. BUT THE PART YOU WANT IS SUBFIELD A. YOU COULD DELETE (OR NOT RECORD) THE REST.

SO IN BND_PUBLICO THE UDC STRING IS: 741(=1:469)"17"(084.11). IN CATALOG_BNP THE UDC STRING IS: 550. IN PORBASE THE UDC STRING IS: 38.

I WOULD MAKE A SPREADSHEET OR DATABASE OF EACH RECORD WITH THREE COLUMNS: IDENTIFIER, UDC NUMBER, DATE OF PUBLICATION.

RUN STATISTICS AND CHARTS ON DATES OF PUBLICATION IN EACH OF THE THREE CATALOGS

RUN BASIC STATISTICS ON UDC MAIN NUMBERS FOR EACH RECORD IN EACH CATALOG, TO CREATE “POPULATION OF THE UDC” IN EACH CATALOG

IN UDC IN ACTION FIGURE 1 SHOWS THE POPULATION OF THE MAIN CLASSES IN OCLC, LEUVEN, AND THE MRF, SO REPLICATE THAT IN EACH OF THESE THREE. USE THE FIRST THREE DIGITS IN FIELD 675. IN BND_PUBLICO THIS IS 741. IN CATALOG_BNP THIS IS 550. IN PORBASE THIS IS 38. ETC.

YOU CAN COUNT THE LENGTH OF THE UDC STRINGS IF YOU WANT. WE REPORTED THAT IN UDC IN ACTION.

YOU CAN CREATE THE SAME NETWORK MATRIX YOU CREATED FOR UDC IN ACTION BY RECORDING THE AUXILIARY OPERATORS AND CONNECTIONS WITHIN THE STRINGS. DO YOU STILL HAVE THE MATRIX FROM BEFORE?

IT WOULD BE HELPFUL FOR ME TO KNOW HOW MANY RECORDS ARE IN EACH FILE.

I CAN REPLICATE MY CLASSIFICATION INTERACTION METHODOLOGY BY DOWNLOADING BIBLIOGRAPHIC CHARACTERISTICS FROM EACH RECORD.


