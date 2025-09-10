import re

# This file contains the regex patterns used in PCBuilder app

numberPattern        = re.compile(r'\d+')
decimalNumberPattern = re.compile(r'\d+(?:[.]\d+)?')


cpuModelPattern = re.compile(r'\d{3,5}\w{0,3}', re.IGNORECASE) # e.g. 7800X3D, 245, 14700k


gpuModelPrefixPattern = re.compile(r'(RTX|RX|Arc)', re.IGNORECASE)
gpuNamePattern        = re.compile(r'(.+?)(GeForce|Radeon|Arc)', re.IGNORECASE) # e.g. SHADOW 3X OC GeForce
gpuModelPattern       = re.compile(rf'{gpuModelPrefixPattern.pattern}\s(\w{{4}})(\s(Ti SUPER|Ti|SUPER|XTX|XT|GRE))?', 
    re.IGNORECASE)                                                              # e.g. RTX 4060 Ti SUPER, RX 6600


ramNamePattern   = re.compile(rf'(.+?)({numberPattern.pattern})\s(GB)', re.IGNORECASE)
ramModulePattern = re.compile(rf'({numberPattern.pattern})\s(x)\s({numberPattern.pattern})(GB)', re.IGNORECASE)
ramSpeedPattern  = re.compile(rf'(DDR2|DDR3|DDR4|DDR5|DDR)(-)({numberPattern.pattern})', re.IGNORECASE)


coolerNamePattern  = re.compile(rf'(.+?)({decimalNumberPattern.pattern})\s(CFM)', re.IGNORECASE)
coolerTypePattern  = re.compile(r'(Yes|No)', re.IGNORECASE)
coolerWidthPattern = re.compile(rf'({numberPattern.pattern})\s(mm)', re.IGNORECASE)


storageSizePattern = re.compile(rf'({decimalNumberPattern.pattern})\s(TB)', re.IGNORECASE)
storageNamePattern = re.compile(rf'(.+?)({decimalNumberPattern.pattern})\s(TB|GB)', re.IGNORECASE) # e.g. Caviar
    # Blue 4.096 TB


caseNamePattern          = re.compile(rf'(.+?)(MicroATX|ATX|Mini ITX)', re.IGNORECASE)
caseMaxGPULengthPattern  = re.compile(rf'{coolerWidthPattern.pattern}', re.IGNORECASE)
caseExpansionSlotPattern = re.compile(rf'({numberPattern.pattern})\s(x)\s(Full-Height via Riser|Full-Height)', 
    re.IGNORECASE)
caseDimensionsPattern    = re.compile(rf'({decimalNumberPattern.pattern})\smm\sx\s'
    rf'({decimalNumberPattern.pattern})\smm\sx\s'
    rf'({decimalNumberPattern.pattern})\smm', re.IGNORECASE)
    

psuNamePattern       = re.compile(rf'(.+?)({numberPattern.pattern})\s(W)', re.IGNORECASE)