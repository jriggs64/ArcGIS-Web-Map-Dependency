# Author: jmriggsbee
# Create Date: 2/7/2024
# Edit Date: 2/16/2024
# Description: Create a relational csv that shows the dependencies between web maps and map/feature services.

import arcgis
import collections
from arcgis.gis import GIS
import pandas as pd
import os
import sys
import json

# List organizations
ma = r'https://org1.maps.arcgis.com'
maUN = 'admin1'
maPW = 'password'
aa = r'https://org2.maps.arcgis.com'
aaUN = 'admin2'
aaPW = 'password'

# Create dictionary of organization URL's: UN, PW, and Organization Abbreviation. 
orgs = {ma: [maUN, maPW, 'MAIN_AGOL'], aa: [aaUN, aaPW, 'AUX_AGOL']}
master = []
masterwm = []
for k, v in orgs.items():
    orgName = v[2]
    gis = GIS(k, v[0], v[1])
    webMaps = gis.content.search(query="", item_type="Web Map", max_items = 10000)
    l = []
    c = []
    count = len(webMaps)
    print(f"{orgName} Map Count: {count}")
    for wm in webMaps:
        wmo = arcgis.mapping.WebMap(wm)
        # ops_layers = wmo['operationalLayers'] # error with operational layers
        ops_layers = wmo.layers
        # add to capture feature collections
        # ops_layers_collections =
        # add to capture raster layers
        # ops_raster_layers =
        # basemap_layers = wmo['baseMap']['baseMapLayers']
        c2 = collections.OrderedDict()
        wmData = wm.get_data()
        path = r"\\Shared-Drive\Backup\WebMaps\{}".format(orgName)
        mapTitle = wm.title.replace(" ", "_").replace(",", ".").replace("&", "and").replace(r"/", "_or_").replace(r"-","_").replace(r"?","").replace(r"|", "").replace(r"(", "").replace(r")", "").replace("__","_")
        name = f"{mapTitle}_{wm.itemid}.json"
        filename = os.path.join(path,name)
        with open(filename, "w") as json_file:
            json.dump(wmData, json_file, indent=4)
        print(f"Created JSON file for {wm.title}")
        try:
            c2["Web Map Name"] = wm.title
        except KeyError:
            c2["Web Map Name"] = 'No Title'
            continue
        try:
            c2["Web Map Item ID"] = wm.itemid
        except KeyError:
            c2["Web Map Item ID"] = 'No Item ID for Map'
            continue
        c.append(c2)
        masterwm.append(c2)

        for op_layer in ops_layers:
            d = collections.OrderedDict()
            try:
                d["Web Map Name"] = wm.title
            except KeyError:
                d["Web Map Name"] = 'No Title'
                continue
            try:
                d["Web Map Item ID"] = wm.itemid
            except KeyError:
                d["Web Map Item ID"] = 'No Item ID for Map'
                continue
            # add organization URL
            try:
                d["Organization URL"] = k
            except KeyError:
                d["Organization URL"] = 'No Item URL for Map'
                continue
            # add map item URL
            try:
                d["Web Map Item URL"] = k + r'/home/item.html?id=' + wm.itemid
            except KeyError:
                d["Web Map Item URL"] = 'No Item URL for Map'
                continue
            # add map owner
            try:
                d["Web Map Owner"] = wm.owner
            except KeyError:
                d["Web Map Owner"] = 'No Item owner for Map'
                continue
            # add map views
            try:
                d["Web Map Views"] = wm.numViews
            except KeyError:
                d["Web Map Views"] = 'No view information for Map'
                continue
            # add map access type
            try:
                d["Web Map Access"] = wm.access
            except KeyError:
                d["Web Map Access"] = 'No access information for Map'
                continue
            try:
                d["Layer Type"] = "{0}".format(op_layer["layerType"])
            except:
                d["Layer Type"] = 'No Layer Type'
                continue
            # add layer name
            try:
                d["Layer Name"] = op_layer["title"]
            except:
                d["Layer Name"] = 'No Layer Name'
                continue
            # add layer itemid
            try:
                d["Layer Item ID"] = op_layer["itemId"]
            except:
                d["Layer Item ID"] = 'No Layer Item ID'
                continue
            try:
                d["Layer URL"] = op_layer["url"]
            except KeyError:
                d["Layer URL"] = 'Broken Link'
                continue
            # add layer itemid
            try:
               d["Layer Item URL"] = k + r'/home/item.html?id=' + op_layer["itemId"]
            except:
               d["Layer Item URL"] = 'No Layer Item URL'
               continue
            try:
                d["Backup JSON File Path"] = filename
            except:
                d["Backup JSON File Path"] = 'No filename'
                continue
            l.append(d)
            master.append(d)

            # print(orgName, 'dateset')
    df = pd.DataFrame(l)
    df.to_csv(r'\\SharedDrive\OrganizationWebMapDependencies\{0}_webMapDependencies.csv'.format(orgName), index = False)
    print(f'{k} done!')
    dfc = pd.DataFrame(c)
    dfc.to_csv(r"\\SharedDrive\OrganizationWebMapDependencies\{0}_maps.csv".format(orgName), index=False)
    print(f"{orgName} map count done!")
    # this section is to help find maps that have no operational layers, feature collections, layers with links to http, or other
    differences = pd.merge(dfc, df, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
    output_file = r"\\SharedDrive\OrganizationWebMapDependencies\{}_missingDependencies.csv".format(orgName)
    organizationURL = r'https://org1.maps.arcgis.com/home/item.html?id='
    differences['Organization URL'] = k
    differences['Web Map Item URL'] = ''
    differences.to_csv(output_file, index=False)
    print("Non-matching rows saved to", output_file)
    # add master difference for all orgs
    masterMap = pd.DataFrame(masterwm)
    masterMap.to_csv(r'\\SharedDrive\OrganizationWebMapDependencies\master_webMap.csv', index = False)
masterDF = pd.DataFrame(master)
masterDF.to_csv(r'\\SharedDrive\OrganizationWebMapDependencies\master_webMapDependencies.csv', index = False)
differencesmaster = pd.merge(masterMap, masterDF, indicator=True, how='outer').query('_merge=="left_only"').drop('_merge', axis=1)
master_output_file = r"\\SharedDrive\OrganizationWebMapDependencies\master_missingDependencies.csv"
organizationURL = r'https://org1.maps.arcgis.com/home/item.html?id='
differencesmaster['Organization URL'] = k
differencesmaster['Web Map Item URL'] = ''
differencesmaster.to_csv(master_output_file, index=False)