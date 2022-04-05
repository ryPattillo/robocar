from constant import CONSTANTS as C

class Encoder:

  def __init__(self):
    self.ticks_la = 0
    self.ticks_lb = 0
    self.ticks_rb = 0
    self.ticks_ra = 0
    
  def read_encoder(self,channel):
      '''
      callback for reading encoder data
      '''
      # keep track of total clicks
      if channel == C["LEFT_ENCODER_A"]:
          self.ticks_la += 1
      if channel == C["LEFT_ENCODER_B"]:
          self.ticks_lb += 1
      if channel == C["RIGHT_ENCODER_A"]:
          self.ticks_ra += 1
      if channel == C["RIGHT_ENCODER_B"]:
          self.ticks_rb += 1   

  def return_ticks(self):
      return (self.ticks_la, self.ticks_lb,self.ticks_ra,self.ticks_rb)

  def reset(self):
      self.ticks_la = 0
      self.ticks_lb = 0
      self.ticks_rb = 0
      self.ticks_ra = 0