import os,sys

CURRENT = os.path.dirname(os.path.realpath(__file__))
ICONDIR = 'images/icons/map_pins/PNG'

def map_icon(style,color,size,type,direction=''):
    """
    Builds an icon based some downloaded map pin icon set.
    """

    if not style in ['Centered','NotCentered']:
        style = 'Centered'

    if not color in ['Azure','Chartreuse','Pink']:
        color = 'Azure'
    
    if not int(size) in [16,24,32,48,64,128,256]:
        size = '32'

    if not type in ['Ball','Board','Bubble','ChequeredFlag','DrawingPin','Flag1','Flag2','Flag3','Flag4','Flag5','Marker','PushPin1','PushPin2']:
        type='Ball'

    size = str(size)+'x'+str(size)
    icon = 'MapMarker_'+type+'_'+direction+'_'+color+'.png'
    path = os.path.join(CURRENT,ICONDIR,style,size,icon)
    if os.path.isfile(path):
        return path
    else:
        print("Error: Image icon doesn't exist: %s" % path)
        sys.exit()


if __name__=='__main__':
    icon = map_icon('Centered','Azure',32,'PushPin2','Left')
    print(icon)
    icon = map_icon('NotCentered','Azure',32,'PushPin1','Right')
    print(icon)
    icon = map_icon('Centered','Pink',32,'')
    print(icon)
