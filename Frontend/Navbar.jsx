import React from 'react';
import { Activity } from 'lucide-react';

const Navbar = () => {
  return (
    <nav className="bg-gradient-to-r from-teal-400 to-teal-500 px-6 py-4 shadow-md">
      <div className="container mx-auto flex items-center justify-between">
        <div className="flex items-center space-x-3">
          <div className="bg-white p-2 rounded-lg shadow-sm">
            <Activity className="w-6 h-6 text-teal-500" />
          </div>
          <div>
            <h1 className="text-white text-xl font-semibold">Preventive medicine</h1>
            <p className="text-teal-100 text-xs">Thermal Comfort Monitoring</p>
          </div>
        </div>
      </div>
    </nav>
  );
};

export default Navbar;