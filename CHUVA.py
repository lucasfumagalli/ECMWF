import matplotlib.pyplot as plt 
from osgeo import gdal 
from mpl_toolkits.basemap import Basemap 
import numpy as np
from numpy import linspace 
from numpy import meshgrid 
import matplotlib.patheffects as path_effects
import datetime as dt
import matplotlib
from datetime import datetime
from datetime import date
import scipy.ndimage as ndimage
import matplotlib.image as image
import csv
from cpt_convert import loadCPT 
from matplotlib.colors import LinearSegmentedColormap 	
import wget
import matplotlib.patheffects as path_effects
plt.rcParams['axes.xmargin'] = 0
print('\n\nPROGRAMA ECMWF\nMeteorologista: Lucas A. F. Coelho')

now = datetime.now()
hora= now.strftime("%H")
minutos= now.strftime("%M")
dia= now.strftime("%d")
#dia='27'
mes= now.strftime("%m")
ano= now.strftime("%Y")

rodada = '12'

hrs = ['15','39','63','87','111','135','162','186','210','234']

baixar = int(input("\n\n1. Atualizar dados?\n\nEntre 1 para atualizar\nEntre 0 para continuar\n\n", )) 
if baixar == 1:
   for i in range(len(hrs)):
       url = 'https://data.ecmwf.int/forecasts/'+ano+''+mes+''+dia+'/'+rodada+'z/0p4-beta/oper/'+ano+''+mes+''+dia+''+rodada+'0000-'+str(hrs[i])+'h-oper-fc.grib2'
       print(url, '\n')
       file = wget.download(url)


print('\n\n2. Início do processo:', dia,'/',mes,'/',ano,' ',hora,':',minutos,'\n\n')


extent = [-90, -60, -20,10]
min_lon = extent[0]; max_lon = extent[2]; min_lat = extent[1]; max_lat = extent[3]
data_inicial=dt.datetime(int(ano),int(mes),int(dia))

print('\n\n3. Montando figuras\n\n')

for j in range(2):
    for i in range(int(len(hrs))+1):
        if i <9:
           gribi = gdal.Open(''+ano+''+mes+''+dia+''+rodada+'0000-'+hrs[i]+'h-oper-fc.grib2')  
           gribi = gdal.Translate('subsected_grib.grb', gribi, projWin = [min_lon-0.1 , max_lat-0.55, max_lon +0.5, min_lat-0.1])    
        
           gribf = gdal.Open(''+ano+''+mes+''+dia+''+rodada+'0000-'+hrs[i+1]+'h-oper-fc.grib2')  
           gribf = gdal.Translate('subsected_grib.grb', gribf, projWin = [min_lon-0.1 , max_lat-0.55, max_lon +0.5, min_lat-0.1])  


        if i ==9:
           gribi = gdal.Open(''+ano+''+mes+''+dia+''+rodada+'0000-'+hrs[0]+'h-oper-fc.grib2')  
           gribi = gdal.Translate('subsected_grib.grb', gribi, projWin = [min_lon-0.1 , max_lat-0.55, max_lon +0.5, min_lat-0.1])    
        
           gribf = gdal.Open(''+ano+''+mes+''+dia+''+rodada+'0000-'+hrs[9]+'h-oper-fc.grib2')  
           gribf = gdal.Translate('subsected_grib.grb', gribf, projWin = [min_lon-0.1 , max_lat-0.55, max_lon +0.5, min_lat-0.1])  

        fig = plt.figure(figsize=(11,11))
        ax = fig.add_subplot(111)
        if j ==0:
           m = Basemap(llcrnrlon=np.min(-90), llcrnrlat=np.min(-40), urcrnrlon=np.max(-20), urcrnrlat=10)
        if j ==1:
           m = Basemap(llcrnrlon=np.min(-64), llcrnrlat=np.min(-36), urcrnrlon=np.max(-41), urcrnrlat=-20)
        m.readshapefile('/Users/lucasfumagalli/shapefile/BRUFE250GC_SIR','BRUFE250GC_SIR',linewidth=.7,color='#606060')
        m.readshapefile('/Users/lucasfumagalli/shapefile/ne_10m_admin_0_countries','ne_10m_admin_0_countries',linewidth=.7,color='#303030')
        m.drawparallels(np.arange( -90., 90.,5.),labels=[1,0,0,0],fontsize=8,linewidth=0.0,  dashes=[4, 2], color='grey')
        m.drawmeridians(np.arange(-180.,180.,5.),labels=[0,0,0,1],fontsize=8,linewidth=0.0,  dashes=[4, 2], color='grey')     
      #  m.bluemarble()


        if i < 9:  
           data0=data_inicial+dt.timedelta(hours=9+int(hrs[i]))
           data1=data_inicial+dt.timedelta(hours=9+int(hrs[i+1]))
        if i == 9:
           data0=data_inicial+dt.timedelta(hours=9+int(hrs[0]))
           data1=data_inicial+dt.timedelta(hours=9+int(hrs[9])) 

        dia0= data0.strftime("%d")
        mes0= data0.strftime("%m")
        ano0= data0.strftime("%Y")
    
        dia1= data1.strftime("%d")
        mes1= data1.strftime("%m")
        ano1= data1.strftime("%Y")


        for item in range(15):
            dadoi = gribi.GetRasterBand(item+1)
            metadata = dadoi.GetMetadata()
            band_name = metadata['GRIB_COMMENT']
            if str(band_name) == str('(prodType 0, cat 1, subcat 193) [-]'):                       
               chuvai = item+1

            dadof = gribf.GetRasterBand(item+1)
            metadata = dadof.GetMetadata()
            band_name = metadata['GRIB_COMMENT']
            if str(band_name) == str('(prodType 0, cat 1, subcat 193) [-]'):                       
               chuvaf = item+1




    
        chuvai = gribi.GetRasterBand(chuvai)
        chuvai = chuvai.ReadAsArray() 
        chuvai = chuvai*1000

        chuvaf = gribf.GetRasterBand(chuvaf)
        chuvaf = chuvaf.ReadAsArray() 
        chuvaf = chuvaf*1000
      
        chuva = chuvaf - chuvai

    
        x = linspace(min_lon, max_lon, chuva.shape[1])
        y = linspace(max_lat, min_lat, chuva.shape[0])
        x, y = m(*np.meshgrid(x, y))   
    
        precc = ['#FFFFFF','#BEBEBE','#A5A5A5','#969696','#828282',
        '#B4F0FA','#96D2FA','#78B9FA','#3C96F5','#1E6EEB','#1464D2',
        '#0FA00F','#28BE28','#50F050','#73F06E','#B4FAAA','#FFFAAA',
        '#FFE878','#FFC03C','#FFA000','#FF6000','#FF3200','#E11400',
        '#C00000','#6C0500','#870000','#643B32','#643232']
    
        levelstp=[0,.5,1,1.5,2,2.5,5,7.5,10,13,16,20,25,30,35,40,50,60,70,80,90,100,125,150,175,200,250,500,3000]

        plotA = plt.contourf(x, y, chuva, colors=precc, levels=levelstp)
      
        if i < 9:
           plt.title('ECMWF: Precipitação total: '+str(dia0)+'/'+str(mes0)+'/'+str(ano0)+' (mm)',fontweight='bold',fontsize=9,loc='left', va='center')    
        if i == 9:
           plt.title('ECMWF: Precipitação total entre: '+str(dia0)+'/'+str(mes0)+'/'+str(ano0)+' - '+str(dia1)+'/'+str(mes1)+'/'+str(ano1)+' (mm)',fontweight='bold',fontsize=9,loc='left', va='center')    

        xx, yy = np.meshgrid(x, y)     
        if j ==0: 
           filecsv = '/Users/lucasfumagalli/python/gfs.csv'
           nome='BR'
           txtplt=plt.text(-89.6,-38.1, '\nModelo ECMWF\nAtualizado em '+str(dia)+'/'+str(mes)+'/'+str(ano)+' '+str(hora)+':'+str(minutos)+'\nMeteorologista: Lucas A. F. Coelho', ha= 'left', va='center', color='k',fontsize=7,zorder=200)    

        if j ==1:
           filecsv = '/Users/lucasfumagalli/python/gfsSUL.csv'
           nome='SBR'
           txtplt=plt.text(-63.9,-35.9, '\nModelo ECMWF\nAtualizado em '+str(dia)+'/'+str(mes)+'/'+str(ano)+' '+str(hora)+':'+str(minutos)+'\nMeteorologista: Lucas A. F. Coelho', ha= 'left', va='bottom', color='k',fontsize=7,zorder=200)               
           
        Latitude,Longitude = [],[]
        with open(''+str(filecsv)+'') as csvfile:
            reader = csv.DictReader(csvfile,delimiter=',')
            for datai in reader:
                Latitude.append(float(datai['LAT']))
                Longitude.append(float(datai['LON']))
    
        xj, yj = m(Longitude, Latitude)            
     
        xk = linspace(min_lon, max_lon, chuva.shape[1])
        yk = linspace(max_lat, min_lat, chuva.shape[0])
    
     
        for k in range(0,len(Latitude)):
            latslons = [Latitude[k], Longitude[k]]                               
            plot = {'lat': latslons[0], 'lon': latslons[1]}        
     
            lat_idx = np.abs(yk - plot['lat']).argmin()  
            lon_idx = np.abs(xk - plot['lon']).argmin()    
            if chuva[lat_idx, lon_idx] > 0.1:      
               txtplt=plt.text(xj[k],yj[k], 
               ''+'{:.1f}'.format(chuva[lat_idx, lon_idx])+'',
               color='k',va='center', ha='center', fontsize=7.5,zorder=100) 
            
    
    
        fig.text(0.9,0.785,'✆ (45) 32225180\n', fontsize=9, fontweight='bold', color='#3EE45C',ha='right', va='center')    
        fig.text(0.9,0.785,'\n✉ lucasfumagalli@gmail.com', fontsize=9, fontweight='bold', color='#EA4335',ha='right', va='center')    
        
        cax = fig.add_axes([0.9024, 0.22, 0.02, 0.5526])
        fig.colorbar(plotA, shrink=.6, cax=cax) 
        if i <9:
           plt.savefig(''+str(nome)+'_'+str(ano0)+'_'+str(mes0)+'_'+str(dia0)+'.png',bbox_inches='tight', dpi=500, transparent=False)  
           print('3.'+str(i+1)+'. Salvando arquivo '+nome+' '+dia0+'/'+mes0+'/'+ano0+'')

        if i ==9:
           plt.savefig(''+str(nome)+'_'+str(ano0)+'_'+str(mes0)+'_'+str(dia0)+'_'+str(ano1)+'__'+str(mes1)+'_'+str(dia1)+'.png',bbox_inches='tight', dpi=500, transparent=False)              
           print('3.'+str(i+1)+'. Salvando arquivo '+nome+' '+dia0+'/'+mes0+'/'+ano0+'_'+nome+' '+dia1+'/'+mes1+'/'+ano1+'')
        plt.clf()
        plt.close()       

print('\n\n4. Arquivos salvos\n\n')
