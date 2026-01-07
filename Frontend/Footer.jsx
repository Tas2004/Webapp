import React from 'react';

const Footer = () => {
  return (
    <footer className="bg-gradient-to-r from-teal-400 to-teal-500 px-6 py-6 mt-auto">
      <div className="container mx-auto">
        <div className="flex flex-col md:flex-row justify-between items-center text-white">
          <div className="mb-4 md:mb-0">
            <h3 className="text-lg font-semibold">Thermal Comfort Prediction System</h3>
            <p className="text-sm text-teal-100">AI-powered patient environment optimization</p>
          </div>
          <div className="text-sm text-teal-100">
            ©2024 MediCare Hospital System. All rights reserved
          </div>
        </div>
      </div>
    </footer>
  );
};

export default Footer;