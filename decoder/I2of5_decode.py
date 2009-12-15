
import scipy
import math

#defining the 10 possible codes.
code0 = ['n','n','w','w','n']
code1 = ['w','n','n','n','w']
code2 = ['n','w','n','n','w']
code3 = ['w','w','n','n','n']
code4 = ['n','n','w','n','w']
code5 = ['w','n','w','n','n']
code6 = ['n','w','w','n','n']
code7 = ['n','n','n','w','w']
code8 = ['w','n','n','w','n']
code9 = ['n','w','n','w','n']
codes = [code0, code1, code2, code3, code4, code5, code6, code7, code8, code9 ]

def value_map( i, j ):
    
    # maps from code index to the corresponding value.
    # 0 <= i < 10
    # 0 <= j < 10
    
    return i*10+j

def l2norm( x ):
    
    sum = 0.0
    for k in range(len(x)):
        sum += x[k]*x[k];
    return math.sqrt(sum/len(x))

def l1norm( x ):
    
    sum = 0.0
    for k in range(len(x)):
        sum += abs(x[k]);
    return sum/len(x)


norm = l2norm

class I2of5_decode:
    # decode one code of interleaved 2 of 5,
    # http://en.wikipedia.org/wiki/Interleaved_2_of_5
    # 
    # 
    
    #parameters:
    #norm = l2norm
    
    mean_level = 2.5
    first_level = 1.0
    mean_level_weight = 1.0
    first_level_weight = 0.3
    
    ref_signals = []
    ref_values = []
    
    def load_shapes( self, narrow_shape, wide_shape ):
        
        self.ref_signals = []
        
        for i in range(10):
            for j in range(10):
                
                signal = scipy.array([])
                
                for k in range(5):
                    
                    if ( codes[i][k] == 'n' ):
                        signal = scipy.append( signal, narrow_shape )
                    else:
                        signal = scipy.append( signal, wide_shape )
                    
                    if ( codes[j][k] == 'n' ):
                        signal = scipy.append( signal, scipy.zeros(len(narrow_shape)) )
                    else:
                        signal = scipy.append( signal, scipy.zeros(len(wide_shape)) ) 
                
                signal /= norm(signal);
                
                self.ref_signals.append( signal )
                self.ref_values.append( value_map(i,j) )
    
    
    def decode( self, signal_in ):
        
        # return data
        certainty = 0
        value = 0
        
        # condition signal_in
        signal_in = scipy.array(signal_in)
        if len(signal_in) != len(self.ref_signals[0]):
            signal_in = signal_in[0:len(self.ref_signals[0])]
        signal_in /= norm(signal_in)
        
        # compute signal distances
        distances = []
        
        for k in range(100):
            distances.append( norm(ref_signals[k] - signal_in) )
        
        #check that there's only one minimum
#        minimum = min(distances)
#        min_count = 0
        
#        for k in range(100):
#            if (distances[k] == minimum ):
#                min_count += 1
        
#        if ( min_count > 1 ):
#            raise Exception("Error: more than one minimum found.")
        
        #get value
        min_index = distances.index( min(distances) )
        value = self.ref_values[ min_index ]
        
        #statistical wizardry for certainty
        
        distances.sort()
        
        minimum = distances[0]
        distances = [ d - minimum for d in distances ]
        
        stdev = scipy.std(distances)
        
        distances = [ d/stdev for d in distances ]
        
        mean = scipy.mean(distances)
        
        certainty = (self.mean_level_weight*mean/self.mean_level + self.first_level_weight*distances[1]/self.first_level) / (self.mean_level_weight + self.first_level_weight)
        
        return [ value, certainty ]
        
        
        
        
