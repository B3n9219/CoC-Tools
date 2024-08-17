import requests
import spreadsheet as sheet
import members
from settings import *
import capital

sheetHeadingOffset = 2

apiKey = "eyJ0eXAiOiJKV1QiLCJhbGciOiJIUzUxMiIsImtpZCI6IjI4YTMxOGY3LTAwMDAtYTFlYi03ZmExLTJjNzQzM2M2Y2NhNSJ9.eyJpc3MiOiJzdXBlcmNlbGwiLCJhdWQiOiJzdXBlcmNlbGw6Z2FtZWFwaSIsImp0aSI6IjZhZDAyZTc1LWIzMjctNGM3Yi1iNzljLWJiOTNkMzY4MWYyMyIsImlhdCI6MTcyMzMwMjMzMiwic3ViIjoiZGV2ZWxvcGVyL2E1Yjc0NTA2LWI3ZDQtZmE3OC0yMmU1LTMwYTg3OTM3YzBlYiIsInNjb3BlcyI6WyJjbGFzaCJdLCJsaW1pdHMiOlt7InRpZXIiOiJkZXZlbG9wZXIvc2lsdmVyIiwidHlwZSI6InRocm90dGxpbmcifSx7ImNpZHJzIjpbIjE0Ny4xNDcuOTIuNDMiXSwidHlwZSI6ImNsaWVudCJ9XX0.tObIRu64OrHg2tVMB6Ry4SPBGWQIvsRJNto3Z_9IO8V0pUMGgJoXRgLQl6phL_4sGGyVfYVpclo0Dre3e438YA"
playerRequestURL = "https://api.clashofclans.com/v1/players/%23"  #followed by player tag (no #)
clanRequestURL = "https://api.clashofclans.com/v1/clans/%23"  #followed by clan tag (no #)


#updates the member sheet's member list
#update_settings()
#members.update_spreadsheet_member_list()
members.update_member_sheet()
#capital.update_capital()