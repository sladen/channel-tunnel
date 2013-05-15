#!/usr/bin/env python
# Paul Sladen 2013-05-12
import math
# Korittke, N.; "Influence of horizontal Refraction on the traverse Measurements
# in Tunnels with Small Diameters"
# 
# Institute for Deposits and Surveying, DMT, Bochum, W-Germany
# http://www.slac.stanford.edu/econf/C9009106/papers/023.PDF
earth_radius = 6378137
bt = {'Great Britain 1989-03 Zig-Zag-Traverse': {
        # WGS84, corner of top of ramp, from Bing imagery/OSM mapping
        'initial': ('A2/1', 51.106436,1.2782455),
        'data': (
        # Probably Channel Tunnel Grid
        # Each ring-number is 1.5-metres in length
        ("A2/2",49.4450,0.372), 
        ("MTS2",56.5071,0.499), # Base of Adit A2
        ("MTS1",122.8067,0.655),  # Base of Adit A1
        ("17",119.81560,1.042),
        ("203",121.4786,1.302),
        ("345",120.8653,1.516),
        ("384",128.1011,1.575),
        ("423",119.5116,1.634),
        ("485",127.8503,1.728),
        ("548",123.1891,1.822),
        ("644",128.8531,1.967),
        ("691",124.4496,2.038),
        ("770",131.4425,2.158),
        ("852",128.4224,2.280),
        ("952",133.2877,2.431),
        ("1113",130.6273,2.673),
        ("1280",132.7052,2.924),
        ("1389",130.0523,3.088),
        ("1680",132.2658,3.526),
        ("1775",129.8136,3.669),
        ("1880",133.3176,3.827),
        ("2070",130.7208,4.113),
        ("2175",133.3090,4.271),
        ("2469",131.0453,4.713),
        ("2569",133.3729,4.863),
        ("2695",130.2317,5.052),
        ("2815",133.0986,5.232),
        ("3066",130.9558,5.609),
        ("3178",133.2237,5.777),
        ("3289",130.1029,5.944),
        ("3410",131.6857,6.126),
        ("3315",131.6927,6.284),
        ("3360",131.6781,6.487)
        )},
      'Great Britain 1989-12 Centre-Line-Traverse': {
        # WGS84, centre of top of ramp via Bing imagery/OSM mapping
        'initial': ('A2T', 51.106446,1.2781995),
        'data': (
        # Probably Channel Tunnel Grid
        # Each ring-number is 1.5-metres in length
        ("A2M",50.9911,0.496),
        ("ENT",120.5663,0.762),
        ("T5",120.7411,1.031),
        ("171",120.4814,1.255),
        ("296",121.4060,1.443),
        ("436",123.5396,1.654),
        ("568",125.7719,1.855),
        ("709",127.6997,2.066),
        ("859",130.1423,2.292),
        ("1018",131.6562,2.531),
        ("1294",131.6672,2.946),
        ("1548",131.6636,3.328),
        ("1827",131.6631,3.748),
        ("1982",131.6358,3.981),
        ("2095",131.6327,4.151),
        ("2234",131.6988,4.360),
        ("2369",131.5948,4.563),
        ("2498",131.6456,4.756),
        ("2622",131.6204,4.943),
        ("2868",131.6293,5.312),
        ("3121",131.6624,5.693),
        ("3270",131.6767,5.916),
        ("3410",131.6813,6.127),
        ("3682",131.6758,6.536),
        ("3850",131.6875,6.787),
        ("4036",131.6758,7.068),
        ("4297",131.6532,7.461),
        ("4441",129.5053,7.677),
        ("4584",126.1020,7.893),
        ("4728",127.2179,8.109),
        ("4868",130.6272,8.319),
        ("5008",133.9648,8.530),
        ("5139",137.1472,8.727),
        ("5279",136.4754,8.938),
        ("5419",133.1182,9.148),
        ("5546",131.6829,9.339),
        ("5722",131.6894,9.412),
        ("5857",131.6793,9.615),
        ("5994",132.5355,9.821),
        ("6136",134.6789,10.035),
        ("6268",136.8510,10.234),
        ("6412",139.0447,10.447),
        ("6558",141.3381,10.670),
        ("6705",143.7011,10.890),
        ("6846",145.9892,11.103),
        ("6985",147.6905,11.312),
        ("7187",147.8379,11.615),
        ("7392",147.8528,11.924),
        ("7574",147.8278,12.198),
        ("7725",147.8456,12.425),
        ("7903",147.8596,12.692),
        ("8050",147.8313,12.913),
        ("8222",147.8339,13.172),
        ("8396",147.8538,13.433),
        ("8544",147.8352,13.656))
        }
}

output = """<?xml version="1.0" encoding="UTF-8"?>
<gpx version="1.0">\n"""
number = 1
for name, survey in bt.items():
    bearing_traverse = survey['data']
    initial_latlon = survey['initial'][1:3]
    initial_name = survey['initial'][0]
    year_month = name[name.index('1989'):name.index('1989')+7]
    lat1, lon1 = math.radians(initial_latlon[0]), math.radians(initial_latlon[1])
    R = earth_radius
    path = [(initial_latlon[0], initial_latlon[1], initial_name)]
    output += """<wpt lat="%f" lon="%f"><name>%s</name></wpt>\n""" % path[-1]
    already_traversed = 0
    for ring, bearing, traverse in bearing_traverse:
        # surveyors use gradians (gon) 
        brng = math.radians(bearing*360/400)
        d = 1000 * (traverse - already_traversed)
        # based on http://www.movable-type.co.uk/scripts/latlong.html#destPoint
        # the original fails to mention that you need to work in radians everywhere
        # which is obvious, I guess
        lat2 = math.asin( math.sin(lat1)*math.cos(d/R) + math.cos(lat1)*math.sin(d/R)*math.cos(brng) )
        lon2 = lon1 + math.atan2(math.sin(brng)*math.sin(d/R)*math.cos(lat1), math.cos(d/R)-math.sin(lat1)*math.sin(lat2));

        path.append((math.degrees(lat2),math.degrees(lon2),ring))
        already_traversed = traverse
        lat1, lon1 = lat2, lon2
        output += """<wpt lat="%f" lon="%f"><name>%s</name></wpt>\n""" % path[-1]
    output += """<time>%s-31T00:00:00Z</time>
<trk><name>%s</name><number>%d</number><trkseg>\n""" % (year_month, name, number)
    for p in path:
        output += """<trkpt lat="%f" lon="%f"></trkpt>\n""" % p[0:2]
    output += """</trkseg></trk>\n"""
    number += 1
output += """</gpx>\n"""
print output
