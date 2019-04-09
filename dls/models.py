class MonomerDimer:
    
    def __init__(self,M_h=1.,M_d=2.,C_tot=100.e-6,R_h=7.3e-9,R_d=13.e-9):
        """ class for extracting monomer-dimer populations from DLS data 
        
            Arguments:
                M_h   -- mass of monomer
                M_d   -- mass of dimer
                C_tot -- total concentration of protein
                R_h   -- expected R_h of monomer
                R_d   -- expected R_h of dimer
        
        """
        self._M_h = M_h
        self._M_d = M_d
        self._C_tot = C_tot
        self._R_h = R_h
        self._R_d = R_d
        
    @property
    def M_h(self):
        return self._M_h
    
    @property
    def M_d(self):
        return self._M_d
    
    @property
    def C_tot(self):
        return self._C_tot

    @property
    def R_h(self):
        return self._R_h
    
    @property
    def R_d(self):
        return self._R_d
    
    def dimer(self, r_avg):
        """ Calculate dimer concentration 
            
            Arguments:
            r_avg -- observed r_h
            
            Returns:
            concentration of dimer
            
        """
        chi_h = r_avg / self.R_h
        chi_d = r_avg / self.R_d
        phi_h = self.M_h**2. / (self.M_h**2. * self.C_tot)
        phi_d = self.M_d**2. / (self.M_h**2. * self.C_tot)
        return (1. - chi_h) / (phi_d * (chi_d - 1.) + 2. * phi_h * (1. - chi_h) )
    
    def monomer(self, r_avg):
        """ Calculate monomer concentration 
        
            Arguments:
            r_avg -- observed r_h
            
            Returns:
            concentration of monomer
        """
        conc_dimer = self.dimer(r_avg)
        return self.C_tot - 2.*conc_dimer

