# OpenBench Stats

## Usage
Use `python3 summary.py --help` to get a full description of options.

#### Basic usage
```
python3 summary.py --instance https://chess.swehosting.se --test 2581
> CREATOR: Littleguineapig
> ENGINE : Willow
> URL    : https://chess.swehosting.se/test/2581
> DIFF   : https://github.com/Adam-Kulju/Willow/compare/8a4c2972..8815e718
>
> ID  :OWNER       :GAMES :WINS  :LOSSES:DRAWS
> 111 :Johan       :1056  :225   :229   :602
> 114 :Johan       :736   :154   :171   :411
> 115 :Dede1751    :510   :101   :119   :290
> 122 :Zuppa       :1930  :400   :396   :1134
> 124 :Johan       :624   :121   :169   :334   <-- Most Anomalous Worker
> 127 :Spamdrew    :140   :25    :20    :95
> 134 :Jay         :5326  :1231  :1125  :2970
>
> Anomaly detected, SPRT rejected.
>
> Possible SPRT Results
> [0,  3] LLR -0.03
> [0,  5] LLR -0.51
> [0, 10] LLR -3.29
```