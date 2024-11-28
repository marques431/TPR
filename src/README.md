# Exfiltration Bot

## sampling.py

### Run

``` sh
python3 sampling.py -i <capture.pcap> -o <sampled_data.txt>
```

> **Nota:** o ficheiro da captura tem de estar em ./captures e o ficheiro de output vai ser gravado na em ./sampled_data

### Output

```
upload_packets upload_bytes download_packets download_bytes
...
```


## features.py 

### Run

```sh
python3 features.py -i <samped_data.txt>
```

> **Nota:** o ficheiro de input tem de estar em ./sampled_data

### Output

\# Features x # Sampled Values x # Windows 
(Ver a ordem)
