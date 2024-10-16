from Scripts.device import device
from who_is_on_my_wifi import *

dev = device()

print(f"""
PC Name:            {dev[0]}
PC Product-Name:    {dev[1]}
MAC Address:        {dev[2]}
IP Address (host):  {dev[3]}
IP Address:         {dev[4]}
Public IP:          {dev[5]}
PC HostName:        {dev[6]}
WiFi Name:          {dev[7]}
Gateway:            {dev[8]}
DNS 1:              {dev[9]}
DNS 2:              {dev[10]}
Password:           {dev[11]}
Security:           {dev[12]}
Interface:          {dev[13]}
Frequency:          {dev[14]}
Signal:             {dev[15]}
Channel:            {dev[16]}


Country:            {dev[17]}
Region:             {dev[18]}
City:               {dev[19]}
Zip Code:           {dev[20]}
Latitude:           {dev[21]}
Longitude:          {dev[22]}
Map:                {dev[23]}
ISP:                {dev[24]}
""")