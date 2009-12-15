
import sys
import math
import numpy
import scipy
import pylab

from I2of5_decode import *
from pysignal import *


    def interpolate_linear(self, t):
        # linear interpolation
        if ( isinstance(t,list) ):
            return [ self.interpolate_linear(t_i) for t_i in t ]
        else:
            i1 = self.index_down(t)
            i2 = self.index_up(t)
            if i1 == i2:
            	return self.data[i1]
            t1 = self.time(i1)
            t2 = self.time(i2)
            y1 = self.data[i1]
            y2 = self.data[i2]
            return (y2-y1)*(t-t1)/(t2-t1)+y1

def averaging_downsample( data_in, initial_time_in, sampling_period_in, intial_time_out, sampling_period_out ):
    
    final_time_in = sampling_period_in*(len(data_in)-1)+initial_time_in
    
    len_data_out = int(math.ceil((final_time_in-initial_time_in)/sampling_poriod_out))
    data_out = numpy.array(len_data_out)
    
    k=0
    t = out_initial_time
    while( t <= in_initial_time and k < len_data_out )
        data_out[k] = 0.0
        k += 1
        t = sampling_period_out*k + out_initial_time
    
    while( t <= final_time_in and k < len_data_out )
        data_out[k] = 
        k += 1
        t = sampling_period_out*k + out_initial_time
    
    
        i1 = int(floor( (t-in_initial_time)/in_sampling_period ))
        i2 = int(ceil( (t-in_initial_time)/in_sampling_period ))
    
    int(floor( (t-self.initial_time)/self.sampling_period ))
    int(ceil((t-self.initial_time)/self.sampling_period))
    
    
    return [ data_out, initial_time_out, sampling_period_out ]




class decoder:
    #
    
    narrow_shape = []
    wide_shape = []
    symbol_decoder = I2of5_decode()
    
    haar_signal = pysignal()
    
    wide_period = 0
    
    # for integration, samples per haar_period=wide_period/len(wide_shape)
    resample_rate = 100
    
    
    def load_shapes( self, narrow_shape_, wide_shape_, wide_period_ ):
        
        self.wide_period = wide_period_
        self.narrow_shape = narrow_shape_
        self.wide_shape = wide_shape_
        
        self.symbol_decoder.load_shapes(  self.narrow_shape, self.wide_shape  )
    
    
    def new_signal( self, signal_in ):
        
        if not isinstance(signal_in, pysignal ):
            raise Exception("Error: input needs to be a pysignal.")
        
        signal = pysignal()
        signal.initial_time = signal_in.initial_time
        dt = self.wide_period/(len(self.wide_shape)*self.resample_rate)
        signal.sampling_period = dt
        signal.data = numpy.zeros( signal_in.total_time()/dt )
        
        for i in range(len(signal.data)):
            signal.data[i] = signal_in.interpolate_linear( signal.time(i) )
        
        self.haar_signal.initial_time = signal.initial_time
        self.haar_signal.sampling_period = self.wide_period/len(self.wide_shape)
        self.haar_signal.data = numpy.zeros( len(signal.data)/self.resample_rate )
        
        k=0
        while self.resample_rate*(k+1) < len(signal.data):
            sum = 0
            for j in range(self.resample_rate):
                sum += signal.data[k*self.resample_rate+j]
            
            self.haar_signal.data[k] = sum/self.resample_rate
            k += 1
    
    
    def decode( time_0 ):
        i0 = haar_signal.index_down(time_0)
        return self.symbol_decoder.decode( haar_signal.data[ i0:len(haar_signal) ] )
        
        
        
    
    
    
    





