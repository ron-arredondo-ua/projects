# Readme for kubernetes tool scripts

# Prerequistes
Kubenetes CLI credentials are required

# Retrieve alert yaml based on namespace, rule and subrule
./get_alert.py

usage: get_alert.py [-h] [-d] -n NAMESPACE -r RULE -s SUBRULE

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug
  -n NAMESPACE, --namespace NAMESPACE
  -r RULE, --rule RULE
  -s SUBRULE, --subrule SUBRULE

example: ./get_alert.py -r prometheusrule -s elasticsearch-exporter-alerter.rules.yaml -n monitoring


# Retrieve a summary of all alerts based on namespace and rule
./get_all_alerts.py

usage: get_all_alerts.py [-h] [-d] -n NAMESPACE -r RULE [-v]

optional arguments:
  -h, --help            show this help message and exit
  -d, --debug
  -n NAMESPACE, --namespace NAMESPACE
  -r RULE, --rule RULE
  -v, --verbose

example: ./get_all_alerts.py -r prometheusrule -n monitoring
