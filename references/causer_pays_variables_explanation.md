# Variables List file
The Variables List file contains a list of the measurement "variable" measurement types.

Column C in the FCAS\_\*.csv file relates back to the number of each variable on the Variables List in order to identify the relevant measurement type of the data in the dynamic data file.

The broad measurement types are:
- Power (MW)
- System Frequency (Hz)
- Electrical Time Error (Seconds)
- Area Control Error (Calculated out of AGC as a MW excess or deficiency)
- Regulation Participation Factor (%)
- Modes of operation (eg.AGC ON, or AGC OFF)
- Column B of the Variables List contains acronyms for the variables, and are briefly defined as follows:

## MW
- MW typically for Interconnectors and Loads.

## Gen MW
- MW used to distinguish Generator output.

## GenSPD MW 
- MW as the Generator SPD 5-minute basepoint (fixed) dispatch target.

## GenRegComp MW 
- MW expressed for the individual Generator Regulation Component.

## SPD MWB 
- MW as the Generator or Interconnector SPD basepoint target. This is effectively identical to GenMW or MW but is obtained directly from SPD and not via the AGC. These devices are not usually dispatchable.

## GenRPF_%
- Regulation Participation factor (%) per Generator. The aggregate of all generators providing frequency regulation should always make 100%. The RPF is a measure of how much regulation (MW) is available.

## ON
- Something that is "ON". It is only ON if the associated Value is not zero. This term is used to identify if AGC is active at the monitored site.

## OFF
- Something that is marked OFF if the associated Value is non-zero. This type is not yet used.

## ACE
- Used for the AGC calculated AreaControlError. The sign of the ACE defines if there is a MW deficiency (-ve) or MW excess (+ve).

## ACEFIL
- A (low-pass) filtered ACE. The ACE is very dynamic and the filtered ACE gives a better representation of which way the ACE is going.

## ACEINT
- The integral of ACE over a defined time period (one hour) and is expressed as a MWH.

## HZ
- Used for System frequency measurements and represents the same frequency that AGC uses.

## HZNOM
- Usually the nominal frequency is 50.00000Hz but the AGC may be directed to consider a different nominal frequency for a brief period, usually subsequent to a major disturbance to hasten any time related errors.

## HZOFFSET
- Is used to express the frequency error (the difference between HZ and HZNOM).

## HZDEV
- Derived from HZOFFSET as a measure of deviation.

## SEC
- Used to express (electrical) time errors. The unit is in seconds and is a measure of the difference between electrical time and standard time.
