#!/usr/bin/env python3
from Gaugi.messenger    import LoggingLevel, Logger
from Gaugi              import GeV
import argparse
import sys,os


mainLogger = Logger.getModuleLogger("pythia")
parser = argparse.ArgumentParser(description = '', add_help = False)
parser = argparse.ArgumentParser()

#
# Mandatory arguments
#


parser.add_argument('-o','--outputFile', action='store', dest='outputFile', required = True,
                    help = "The event file generated by pythia.")

parser.add_argument('--evt','--numberOfEvents', action='store', dest='numberOfEvents', required = True, type=int, default=1,
                    help = "The number of events to be generated.")

#
# Pileup simulation arguments
#

parser.add_argument('--pileupAvg', action='store', dest='pileupAvg', required = False, type=int, default=0,
                    help = "The pileup average (default is zero).")

parser.add_argument('--bc_id_start', action='store', dest='bc_id_start', required = False, type=int, default=0,
                    help = "The bunch crossing id start.")

parser.add_argument('--bc_id_end', action='store', dest='bc_id_end', required = False, type=int, default=0,
                    help = "The bunch crossing id end.")

parser.add_argument('--bc_duration', action='store', dest='bc_duration', required = False, type=int, default=25,
                    help = "The bunch crossing duration (in nanoseconds).")


#
# Extra parameters
#

parser.add_argument('--outputLevel', action='store', dest='outputLevel', required = False, type=int, default=0,
                    help = "The output level messenger.")

parser.add_argument('-s','--seed', action='store', dest='seed', required = False, type=int, default=0,
                    help = "The pythia seed (zero is the clock system)")




if len(sys.argv)==1:
  parser.print_help()
  sys.exit(1)

args = parser.parse_args()

from PythiaGenerator import EventGenerator


minbias = os.environ['LZT_PATH']+'/generator/PythiaGenerator/data/minbias_config.cmnd'

generator = EventGenerator( "EventGenerator",
                            OutputFile     = args.outputFile,
                            MinbiasFile    = minbias,
                            EtaMax         = 1.4,
                            Select         = 2,
                            PileupAvg      = args.pileupAvg,
                            BunchIdStart   = args.bc_id_start,
                            BunchIdEnd     = args.bc_id_end,
                            OutputLevel    = args.outputLevel,
                            Seed           = args.seed,
                            )


# Window definition
generator.setProperty("MinbiasDeltaEta",  0.22 )
generator.setProperty("MinbiasDeltaPhi",  0.22 )

# To collect using this cell position
from PythiaGenerator import Seed
seeds = [
          # -0.22 to 0.22
          #Region("Region_1", Eta=0.0, Phi=1.52170894 ),
          # 0.28 to 0.72
          Seed("Seed_2", Eta=0.3, Phi=1.52170894 ),
        ]

# Add seeds. This will be used to collect Minimum bias for this specific regions (seeds)
for seed in seeds:
  generator.push_back(seed)


# Run
generator.run(args.numberOfEvents)



