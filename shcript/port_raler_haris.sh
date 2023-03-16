#!/bin/bash
sudo iptables -t nat -A PREROUTING -p udp --dport 8890 -j DNAT --to-destination 192.168.10.1:8890
sudo iptables -t nat -A PREROUTING -p tcp --dport 8890 -j DNAT --to-destination 192.168.10.1:8890
sudo iptables -t nat -A PREROUTING -p udp --dport 8889 -j DNAT --to-destination 192.168.10.1:8889
sudo iptables -t nat -A PREROUTING -p tcp --dport 8889 -j DNAT --to-destination 192.168.10.1:8889
sudo iptables -t nat -A PREROUTING -p udp --dport 11111 -j DNAT --to-destination 192.168.10.1:11111
sudo iptables -t nat -A PREROUTING -p tcp --dport 11111 -j DNAT --to-destination 192.168.10.1:11111
