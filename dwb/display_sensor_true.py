'''
display_sensor_true.py
Additional changes in the main need to done 

'''



import pygame
from pygame import font
import random


def _content (weight: float)-> list:
    '''input: scale reading (weight)
    returns a list of text that is written in the text bubble'''
    
    CO2_val = weight * 0.3968316
    display_list =  [
    [' ',' ',' ','Thank you for composting!','You just composted '+ str(weight) +  ' ounces!'],
    [' ',' ',' ','Thank you for composting!','You just helped avoid '+ str(CO2_val) + ' ounces of carbon-equivalent emissions! '],
    [' ',' ',' ','Thank you for composting!',' Food waste is the single largest part of waste.',' Keeping it out of landfills is important!']]
    index= random.choice ([0,1,2]) 
    return display_list[index]


def drawText(surface, text_list:list, color, rect, font_height:int, aa=False, bkg=None): 
    # Wraps text and draws it inside the rect. 
    y = rect.top

    #padding ratios have been calculated based on border and image dimensions.
    pad_x= (0.1* rect.width)
    pad_y= (0.1* rect.height)
    pad_y_bottom= (0.24* rect.height)
    
    font= pygame.font.Font(None, font_height)

    for text in text_list:
        while text:
            i = 1
            #determine if the row of text will be outside our area
            if (y + font_height+ (2*pad_y) + pad_y_bottom ) > rect.bottom:
                print("Could not fit in all the text. Please reduce font")
                return

            # determine maximum width of line
            while font.size(text[:i])[0] < (rect.width- pad_x*2) and i < len(text):
                i += 1
            # if we've wrapped the text, then adjust the wrap to the last word

            if i < len(text):
                text_to_find= " "
                i = text.rfind(text_to_find, 0, i)

            #render the line and blit it to the surface
            if bkg:
                image = font.render(text[:(i)], 1, color, bkg)
                image.set_colorkey(bkg)
            else:
                image = font.render(text[:i], aa, color)
            surface.blit(image, (rect.left+pad_x, y+pad_y))
            y += font_height

            # remove the text we just blitted
            text = text[i:]

            

def scale_text_bubble(width, iwidth, height, iheight)->'scale':
    #Scales the image to best fit. Assumed 1/5 of the screen as pad_x and pad_y

    scale_x= ((3/5)*width)/iwidth
    scale_y= ((3/5)*height)/iheight
    scale = min(scale_x,scale_y)
    if scale<1:
        scale=1
    return scale



def draw_text_bubble(screen,width,height)-> []:
    # draws a text bubble with sufficient x and y padding. This function returns a list containing the surface, x_pad val and y_pad val.

    text_bubble = pygame.image.load ('/home/pi/DigitalWasteBins/dwb/images/text_bubbles_transparent/box_white.png')
    iwidth,iheight= text_bubble.get_size()

    scale = scale_text_bubble(width, iwidth, height, iheight)
    text_bubble = pygame.transform.scale(text_bubble, (int(scale*iwidth), int(scale*iheight)))
    swidth, sheight= text_bubble.get_size()

    pad_x= (width-swidth)/2
    pad_y = (1/2)*(height-(sheight))

    screen.blit(text_bubble, (pad_x,pad_y))
    pygame.display.update()
    return [text_bubble, pad_x, pad_y]


if __name__ == '__main__':

    #To be added: if sensor_boolean= True:

    pygame.init()

    '''hardcoded values:
    weight (for now) is set to 10.55 
    font_height will be adjusted to best fit the text in the bubble
    '''
    font_height=30
    weight= 10.55  
    
    screen= pygame.display.set_mode((0,0),pygame.FULLSCREEN)
    width,height= screen.get_size()
    ret_list= draw_text_bubble(screen,width,height)
    text_bubble= ret_list[0]
    x= ret_list[1]
    y= ret_list[2]
    rect= text_bubble.get_rect().move(x,y)

    text_list= _content (weight) 

    drawText(screen, text_list, (128, 128, 128), rect, font_height, aa=False, bkg=None)
    pygame.display.update()

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
                break
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_ESCAPE:
                    running = False
                    break

    pygame.quit()
