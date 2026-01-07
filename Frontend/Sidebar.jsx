import React, { useState } from 'react';
import { Activity, Users, TrendingUp, LogOut } from 'lucide-react';

const Sidebar = () => {
  const [activePage, setActivePage] = useState('patients');

  return (
    <div className="w-64 h-screen bg-gradient-to-r from-teal-400 to-teal-500 px-6 py-4 shadow-md text-white flex flex-col">
      <div className="p-6 border-b border-cyan-400">
        <div className="flex items-center gap-3">
          <Activity className="w-8 h-8" />
          <div>
            <h1 className="text-lg font-bold">Preventive Medicine</h1>
            <p className="text-xs text-cyan-100">Thermal Comfort Monitoring</p>
          </div>
        </div>
      </div>

      {/* Menu Section */}
      <div className="flex-1 p-6">
        <p className="text-xs text-cyan-200 mb-4 font-semibold">Menu</p>

        <nav className="space-y-2">
          {/* Patients Menu Item */}
          <button
            onClick={() => setActivePage('patients')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              activePage === 'patients'
                ? 'bg-cyan-400 bg-opacity-40'
                : 'hover:bg-cyan-400 hover:bg-opacity-30'
            }`}
          >
            <Users className="w-5 h-5" />
            <span className="font-medium">Patients</span>
          </button>

          {/* Prediction Menu Item */}
          <button
            onClick={() => setActivePage('prediction')}
            className={`w-full flex items-center gap-3 px-4 py-3 rounded-lg transition-all ${
              activePage === 'prediction'
                ? 'bg-cyan-400 bg-opacity-40'
                : 'hover:bg-cyan-400 hover:bg-opacity-30'
            }`}
          >
            <TrendingUp className="w-5 h-5" />
            <span className="font-medium">Prediction</span>
          </button>
        </nav>
      </div>

      {/* Logout Button */}
      <div className="p-6">
        <button className="w-full flex items-center gap-3 px-4 py-3 rounded-lg hover:bg-cyan-400 hover:bg-opacity-30 transition-all">
          <LogOut className="w-5 h-5" />
          <span className="font-medium">Log out</span>
        </button>
      </div>
    </div>
  );
};

export default Sidebar;