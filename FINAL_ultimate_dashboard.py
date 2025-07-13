#!/usr/bin/env python3
"""
🌾 ULTIMATE SMART FARMER DASHBOARD - ALL CSV DATA INTEGRATED
===========================================================

Complete agricultural system using:
- crops.csv: 57 crops with full agricultural data
- crop_yield.csv: Detailed yield and harvest information  
- cropping_pattern.csv: Intercropping and rotation patterns
- intercrops.csv: Detailed intercropping combinations
- maintenance.csv: Complete maintenance schedules
- soil_types.csv: Soil characteristics
- region_weather.csv: Regional climate data
- crop_suitability.csv: Crop-soil matching
"""

import http.server
import socketserver
import json
import csv
import os
import sys
import socket
import requests
import webbrowser
from urllib.parse import urlparse, parse_qs, unquote
from datetime import datetime, timedelta

# Weather API configuration
WEATHER_API_KEY = "K4AYL2XZVEG22B5AWZ8EJ6HXC"
WEATHER_API_BASE = "https://weather.visualcrossing.com/VisualCrossingWebServices/rest/services/timeline"

class UltimateSmartFarmerHandler(http.server.SimpleHTTPRequestHandler):
    def __init__(self, *args, **kwargs):
        # Load ALL CSV data when handler is created
        self.load_all_csv_data()
        super().__init__(*args, **kwargs)
    
    def load_all_csv_data(self):
        """Load ALL CSV data from every file in the project"""
        self.data = {
            'crops': [],
            'crop_yield': [],
            'cropping_pattern': [],
            'intercrops': [],
            'maintenance': [],
            'soil_types': [],
            'region_weather': [],
            'crop_suitability': []
        }
        
        # List all possible CSV file names (handle different naming conventions)
        csv_files = {
            'crops': ['crops.csv', 'crop.csv', 'Crops.csv'],
            'crop_yield': ['crop_yield.csv', 'yield.csv', 'Crop_yield.csv'], 
            'cropping_pattern': ['cropping_pattern.csv', 'pattern.csv', 'Cropping_pattern.csv'],
            'intercrops': ['intercrops.csv', 'intercrop.csv', 'Intercrops.csv'],
            'maintenance': ['maintenance.csv', 'Maintenance.csv'],
            'soil_types': ['soil_types.csv', 'soil.csv', 'Soil_types.csv'],
            'region_weather': ['region_weather.csv', 'weather.csv', 'Region_weather.csv'],
            'crop_suitability': ['crop_suitability.csv', 'suitability.csv', 'Crop_suitability.csv']
        }
        
    def load_all_csv_data(self):
        """Load ALL CSV data from every file in the project"""
        # Check what files exist in directory
        print("🔍 Checking directory contents:")
        try:
            current_files = [f for f in os.listdir('.') if f.endswith('.csv')]
            print(f"   Found CSV files: {current_files}")
        except Exception as e:
            print(f"   Error listing files: {e}")
        
        self.data = {
            'crops': [],
            'crop_yield': [],
            'cropping_pattern': [],
            'intercrops': [],
            'maintenance': [],
            'soil_types': [],
            'region_weather': [],
            'crop_suitability': []
        }
        
        # List all possible CSV file names (handle different naming conventions)
        csv_files = {
            'crops': ['crops.csv', 'crop.csv', 'Crops.csv'],
            'crop_yield': ['crop_yield.csv', 'yield.csv', 'Crop_yield.csv'], 
            'cropping_pattern': ['cropping_pattern.csv', 'pattern.csv', 'Cropping_pattern.csv'],
            'intercrops': ['intercrops.csv', 'intercrop.csv', 'Intercrops.csv'],
            'maintenance': ['maintenance.csv', 'Maintenance.csv'],
            'soil_types': ['soil_types.csv', 'soil.csv', 'Soil_types.csv'],
            'region_weather': ['region_weather.csv', 'weather.csv', 'Region_weather.csv'],
            'crop_suitability': ['crop_suitability.csv', 'suitability.csv', 'Crop_suitability.csv']
        }
        
        for data_key, possible_files in csv_files.items():
            loaded = False
            for filename in possible_files:
                if os.path.exists(filename):
                    # Try multiple encodings to handle different file formats
                    encodings = ['utf-8', 'utf-8-sig', 'latin-1', 'cp1252']
                    for encoding in encodings:
                        try:
                            with open(filename, 'r', encoding=encoding) as f:
                                reader = csv.DictReader(f)
                                self.data[data_key] = [row for row in reader]
                                print(f"✅ Loaded {filename} ({encoding}): {len(self.data[data_key])} records")
                                loaded = True
                                break
                        except Exception as e:
                            if encoding == encodings[-1]:  # Last encoding attempt
                                print(f"❌ Error loading {filename} with all encodings: {e}")
                    if loaded:
                        break
            
            if not loaded:
                print(f"⚠️  No file found for {data_key}. Tried: {possible_files}")
                self.data[data_key] = []
        
        # Add sample data if no CSV files are found
        if len(self.data['crops']) == 0:
            print("📝 Adding sample crop data...")
            self.data['crops'] = [
                {
                    'CropID': '1',
                    'CropName': 'Rice (Paddy)',
                    'CropFamily': 'Poaceae',
                    'CropType': 'Cereal',
                    'Seasonality': 'Kharif',
                    'TypicalDuration_days': '120',
                    'SeedRate_kg_per_ha': '30',
                    'IrrigationRequirement_mm': '1200',
                    'MinTemp_C': '20',
                    'MaxTemp_C': '35',
                    'MinSoilpH': '5.5',
                    'MaxSoilpH': '7.0',
                    'SoilType': 'alluvial, clay, red soil',
                    'Sowing Months': 'May-July (Kharif)',
                    'Harvesting Months': 'October-November',
                    'FertilizerDose_kg_per_ha': '100:50:50',
                    'PesticidesUsed': 'Carbendazim, Chlorpyrifos',
                    'Nutrients Required': 'N, P, K, S, Zn, Fe, Mn',
                    'Organic Fertilizer Substitutes': 'FYM, compost, green manure, Azospirillum, PSB, neem cake, vermicompost',
                    'LabourDays_per_ha': '80',
                    'ManureRequirement_ton_per_ha': '10',
                    'Water_Requirement_Min_(mm)': '202',
                    'Water_Requirement_Max_(mm)': '322'
                },
                {
                    'CropID': '2',
                    'CropName': 'Wheat',
                    'CropFamily': 'Poaceae',
                    'CropType': 'Cereal',
                    'Seasonality': 'Rabi',
                    'TypicalDuration_days': '120',
                    'SeedRate_kg_per_ha': '100',
                    'IrrigationRequirement_mm': '400',
                    'MinTemp_C': '10',
                    'MaxTemp_C': '32',
                    'MinSoilpH': '6.0',
                    'MaxSoilpH': '7.5',
                    'SoilType': 'alluvial, black soil, loam',
                    'Sowing Months': 'October-December',
                    'Harvesting Months': 'February-May',
                    'FertilizerDose_kg_per_ha': '120:60:40',
                    'PesticidesUsed': 'Imidacloprid, Tebuconazole',
                    'Nutrients Required': 'N, P, K, S, Zn, Fe',
                    'Organic Fertilizer Substitutes': 'FYM, compost, green manure, Azotobacter, PSB, bone meal, rock phosphate',
                    'LabourDays_per_ha': '70',
                    'ManureRequirement_ton_per_ha': '8',
                    'Water_Requirement_Min_(mm)': '535',
                    'Water_Requirement_Max_(mm)': '1475'
                }
            ]
            
        if len(self.data['soil_types']) == 0:
            print("📝 Adding sample soil data...")
            self.data['soil_types'] = [
                {
                    'soil_id': '1',
                    'name': 'Red Soil',
                    'color_origin': 'Reddish, weathered igneous/metamorphic rocks',
                    'texture_structure': 'Sandy to clayey, often gravelly',
                    'min_ph': '5.5',
                    'max_ph': '6.5',
                    'water_retention': 'Low',
                    'fertility_level': 'Low-Moderate'
                },
                {
                    'soil_id': '2',
                    'name': 'Black Soil',
                    'color_origin': 'Deep black, volcanic (basalt)',
                    'texture_structure': 'Clayey, fine-grained, cracks',
                    'min_ph': '6.5',
                    'max_ph': '8.0',
                    'water_retention': 'High',
                    'fertility_level': 'High'
                }
            ]
            
        if len(self.data['region_weather']) == 0:
            print("📝 Adding sample region data...")
            self.data['region_weather'] = [
                {
                    'region_id': '1',
                    'city_district': 'Udaipur',
                    'climate_zone': 'Subtropical Monsoon',
                    'ann_rain_mm': '600',
                    'min_temp_c': '15',
                    'max_temp_c': '40',
                    'avg_humidity_percent': '65'
                }
            ]
            
        if len(self.data['crop_suitability']) == 0:
            print("📝 Adding sample suitability data...")
            self.data['crop_suitability'] = [
                {
                    'crop_id': '1',
                    'soil_id': '1',
                    'suitability_level': 'High',
                    'reason': 'Red soil is suitable for paddy with proper water management'
                },
                {
                    'crop_id': '1',
                    'soil_id': '2',
                    'suitability_level': 'Very High',
                    'reason': 'Black soil retains water well, ideal for paddy cultivation'
                },
                {
                    'crop_id': '2',
                    'soil_id': '1',
                    'suitability_level': 'Moderate',
                    'reason': 'Red soil can support wheat with additional fertilizers'
                },
                {
                    'crop_id': '2',
                    'soil_id': '2',
                    'suitability_level': 'High',
                    'reason': 'Black soil is fertile and well-suited for wheat'
                }
            ]
        
        print(f"\n🎯 TOTAL DATA LOADED:")
        print(f"   📊 {len(self.data['crops'])} crops with full details")
        print(f"   🌾 {len(self.data['crop_yield'])} yield records")
        print(f"   🔄 {len(self.data['cropping_pattern'])} cropping patterns")
        print(f"   🌿 {len(self.data['intercrops'])} intercrop combinations")
        print(f"   🛠️ {len(self.data['maintenance'])} maintenance steps")
        print(f"   🌱 {len(self.data['soil_types'])} soil types")
        print(f"   🌍 {len(self.data['region_weather'])} regional climates")
        print(f"   ✅ {len(self.data['crop_suitability'])} suitability matches")
    
    def get_weather_data(self, location):
        """Get real weather data from Visual Crossing API"""
        try:
            url = f"{WEATHER_API_BASE}/{location}"
            params = {
                'key': WEATHER_API_KEY,
                'include': 'current,days',
                'elements': 'temp,humidity,precip,windspeed,conditions'
            }
            
            response = requests.get(url, params=params, timeout=10)
            if response.status_code == 200:
                data = response.json()
                current = data.get('currentConditions', {})
                return {
                    'success': True,
                    'temperature': current.get('temp', 'N/A'),
                    'humidity': current.get('humidity', 'N/A'),
                    'conditions': current.get('conditions', 'N/A'),
                    'precipitation': current.get('precip', 0),
                    'windspeed': current.get('windspeed', 'N/A')
                }
            else:
                return {'success': False, 'error': 'API request failed'}
        except Exception as e:
            return {'success': False, 'error': str(e)}
    
    def check_sowing_month(self, crop, current_month):
        """Enhanced month checking logic for sowing seasons"""
        sowing_months = str(crop.get('Sowing Months', '')).lower()
        
        # Month mapping for better matching
        month_names = ['january', 'february', 'march', 'april', 'may', 'june',
                      'july', 'august', 'september', 'october', 'november', 'december']
        
        if isinstance(current_month, str) and current_month.isdigit():
            current_month = int(current_month)
        
        if isinstance(current_month, int) and 1 <= current_month <= 12:
            target_month = month_names[current_month - 1]
            target_month_short = target_month[:3]
        else:
            return False
        
        # Check for month names and abbreviated forms
        if (target_month in sowing_months or 
            target_month_short in sowing_months or
            target_month.capitalize() in sowing_months or
            target_month_short.capitalize() in sowing_months):
            return True
        
        # Check for season-based matching
        seasons = {
            'kharif': [6, 7, 8, 9],  # June to September
            'rabi': [10, 11, 12, 1, 2, 3],  # October to March
            'zaid': [3, 4, 5, 6]  # March to June
        }
        
        crop_seasonality = str(crop.get('Seasonality', '')).lower()
        for season, months in seasons.items():
            if season in crop_seasonality and current_month in months:
                return True
        
        return False

    def find_suitable_crops(self, region_id, soil_id, month):
        """Enhanced crop finding using ALL data - crop_suitability, climate, soil, seasonality"""
        suitable_crops = []
        
        # Get regional climate data
        region = next((r for r in self.data['region_weather'] if str(r.get('region_id', '')) == str(region_id)), None)
        
        # Get soil data
        soil = next((s for s in self.data['soil_types'] if str(s.get('soil_id', '')) == str(soil_id)), None)
        
        # Get ALL crops suitable for this soil from crop_suitability table
        soil_suitable_crops = [s for s in self.data['crop_suitability'] 
                              if str(s.get('soil_id', '')) == str(soil_id) and 
                              s.get('suitability_level') in ['High', 'Very High', 'Moderate']]
        
        # Sort by suitability level
        soil_suitable_crops.sort(key=lambda x: {'High': 0, 'Very High': 0, 'Moderate': 1}.get(x.get('suitability_level', 'Moderate'), 2))
        
        current_month = int(month) if month.isdigit() and 1 <= int(month) <= 12 else 1
        
        for suitability in soil_suitable_crops:
            crop_id = str(suitability.get('crop_id', ''))
            
            # Find the crop details
            crop = next((c for c in self.data['crops'] if str(c.get('CropID', '')) == crop_id), None)
            
            if not crop:
                continue
            
            # Enhanced month checking
            is_suitable_month = self.check_sowing_month(crop, current_month)
            
            if not is_suitable_month:
                continue
            
            # Get additional comprehensive data for this crop
            yield_info = next((y for y in self.data['crop_yield'] if str(y.get('CropID', '')) == crop_id), {})
            pattern_info = next((p for p in self.data['cropping_pattern'] if str(p.get('CropID', '')) == crop_id), {})
            intercrop_info = next((i for i in self.data['intercrops'] if str(i.get('CropID', '')) == crop_id), {})
            
            # Get ALL maintenance steps for this crop
            maintenance_steps = [m for m in self.data['maintenance'] if str(m.get('CropID', '')) == crop_id]
            
            # Combine all data with enhanced crop_suitability information
            enhanced_crop = {
                **crop,
                'yield_info': yield_info,
                'pattern_info': pattern_info,
                'intercrop_info': intercrop_info,
                'maintenance_steps': maintenance_steps,
                'suitability_reason': suitability.get('reason', 'Suitable for selected conditions'),
                'suitability_level': suitability.get('suitability_level', 'High'),
                'region_info': region,
                'soil_info': soil,
                'total_maintenance_steps': len(maintenance_steps)
            }
            
            suitable_crops.append(enhanced_crop)
        
        return suitable_crops[:20]  # Return top 20 matches
    
    def get_maintenance_schedule(self, crop_id):
        """Get complete maintenance schedule for a crop"""
        return [m for m in self.data['maintenance'] if str(m.get('CropID', '')) == str(crop_id)]
    
    def do_GET(self):
        if self.path == '/' or self.path == '/index.html':
            self.serve_ultimate_dashboard()
        elif self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            super().do_GET()
    
    def do_POST(self):
        if self.path.startswith('/api/'):
            self.handle_api_request()
        else:
            self.send_error(404)
    
    def handle_api_request(self):
        """Handle API requests"""
        path = self.path.split('?')[0]
        
        if path == '/api/get-all-data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.data, ensure_ascii=False).encode('utf-8'))
        
        elif path == '/api/comprehensive-recommendations':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            crops = self.find_suitable_crops(
                request_data.get('region_id'),
                request_data.get('soil_id'),
                request_data.get('month')
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'success': True,
                'crops': crops[:15]  # Top 15 comprehensive results
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif path == '/api/maintenance-schedule':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            crop_id = request_data.get('crop_id')
            schedule = self.get_maintenance_schedule(crop_id)
            crop = next((c for c in self.data['crops'] if str(c.get('CropID', '')) == str(crop_id)), {})
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'success': True,
                'schedule': schedule,
                'crop_name': crop.get('CropName', 'Unknown Crop')
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif path == '/api/weather':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            weather_data = self.get_weather_data(request_data.get('location', ''))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(weather_data, ensure_ascii=False).encode('utf-8'))
        
        elif path == '/api/crop-rotation':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
            
            try:
                data = json.loads(body) if body.strip() else {}
                current_crop_id = str(data.get('current_crop_id', ''))
                next_season = data.get('next_season', '')
                
                if not current_crop_id or not next_season:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Missing parameters'}).encode())
                    return

                # Get current crop info
                current_crop = next((c for c in self.data['crops'] if str(c.get('CropID', '')) == current_crop_id), {})
                if not current_crop:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Crop not found'}).encode())
                    return

                # Get recommended rotation crops
                recommended_crops = self.get_rotation_recommendations(current_crop, next_season)
                rotation_rules = [
                    "Avoid planting crops of the same family in sequence",
                    "Alternate surface-feeding with deep-rooting crops", 
                    "Follow root crops with vines or leaf crops",
                    "Choose crops suited to your soil type and pH",
                    "Use legumes to naturally fix nitrogen in soil"
                ]

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_data = {
                    'success': True,
                    'current_crop': current_crop,
                    'recommended_crops': recommended_crops,
                    'rotation_rules': rotation_rules
                }
                
                self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
        
        else:
            self.send_response(404)
            self.end_headers()
    
    def serve_ultimate_dashboard(self):
        """Serve the ultimate comprehensive farmer dashboard"""
        html_content = f"""
<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>🌾 Uncompromized Smart Farmer Dashboard</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <style>
        .gradient-bg {{ background: linear-gradient(135deg, #10b981 0%, #065f46 100%); }}
        .card-hover:hover {{ transform: translateY(-2px); transition: all 0.3s ease; }}
        .fade-in {{ animation: fadeIn 0.5s ease-in; }}
        @keyframes fadeIn {{ from {{ opacity: 0; }} to {{ opacity: 1; }} }}
        .loading {{ border: 3px solid #f3f3f3; border-top: 3px solid #10b981; 
                  border-radius: 50%; width: 20px; height: 20px; animation: spin 1s linear infinite; }}
        @keyframes spin {{ 0% {{ transform: rotate(0deg); }} 100% {{ transform: rotate(360deg); }} }}
        .weather-card {{ background: linear-gradient(135deg, #3b82f6 0%, #1e40af 100%); }}
        .data-grid {{ display: grid; grid-template-columns: repeat(auto-fit, minmax(250px, 1fr)); gap: 1rem; }}
        .stat-card {{ background: linear-gradient(135deg, #8b5cf6 0%, #7c3aed 100%); }}
        @media (max-width: 768px) {{
            .container {{ padding-left: 8px; padding-right: 8px; }}
            .mobile-grid {{ grid-template-columns: 1fr; }}
            .data-grid {{ grid-template-columns: 1fr; }}
        }}
    </style>
</head>
<body class="bg-gray-50">
    <!-- Header -->
    <header class="gradient-bg text-white shadow-lg">
        <div class="container mx-auto px-4 py-6">
            <h1 class="text-3xl font-bold">🌾 Uncompromized Smart Farmer Dashboard</h1>
            <p class="text-green-100 mt-2">Complete Agricultural System - All {len(self.data['crops'])} Crops with Complete Data Integration</p>
            <div class="mt-4 grid grid-cols-2 md:grid-cols-4 gap-4 text-sm">
                <div class="bg-green-600 bg-opacity-50 rounded p-2 text-center">
                    <div class="font-bold text-lg">{len(self.data['crops'])}</div>
                    <div>Crops</div>
                </div>
                <div class="bg-green-600 bg-opacity-50 rounded p-2 text-center">
                    <div class="font-bold text-lg">{len(self.data['soil_types'])}</div>
                    <div>Soil Types</div>
                </div>
                <div class="bg-green-600 bg-opacity-50 rounded p-2 text-center">
                    <div class="font-bold text-lg">{len(self.data['region_weather'])}</div>
                    <div>Regions</div>
                </div>
                <div class="bg-green-600 bg-opacity-50 rounded p-2 text-center">
                    <div class="font-bold text-lg">{len(self.data['maintenance'])}</div>
                    <div>Maintenance Steps</div>
                </div>
            </div>
        </div>
    </header>

    <!-- Navigation -->
    <nav class="bg-white shadow-sm border-b sticky top-0 z-50">
        <div class="container mx-auto px-4">
            <div class="flex flex-wrap justify-center py-4 space-x-2 md:space-x-4">
                <button onclick="showSection('main')" class="nav-btn bg-green-500 text-white px-4 py-2 rounded">
                    🏠 मुख्य / Main
                </button>
                <button onclick="showSection('yield')" class="nav-btn bg-gray-200 text-gray-700 px-4 py-2 rounded">
                    📈 Yield Analysis
                </button>
                <button onclick="showSection('intercrop')" class="nav-btn bg-gray-200 text-gray-700 px-4 py-2 rounded">
                    🌿 Intercropping
                </button>
                <button onclick="showSection('rotation')" class="nav-btn bg-gray-200 text-gray-700 px-4 py-2 rounded">
                    🔄 Crop Rotation
                </button>
                <button onclick="showSection('maintenance')" class="nav-btn bg-gray-200 text-gray-700 px-4 py-2 rounded">
                    🛠️ Maintenance
                </button>
                <button onclick="showSection('weather')" class="nav-btn bg-gray-200 text-gray-700 px-4 py-2 rounded">
                    🌤️ Weather
                </button>
            </div>
        </div>
    </nav>

    <main class="container mx-auto px-4 py-6">
        
        <!-- Main Section -->
        <div id="main" class="section fade-in">
            <div class="bg-white rounded-lg shadow-md p-6 mb-6">
                <h2 class="text-xl font-bold mb-4 text-green-800">🎯 Complete Crop Recommendation System</h2>
                
                <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">📍 Region / स्थान:</label>
                        <select id="region" class="w-full p-3 border border-gray-300 rounded-md" onchange="updateRegionInfo()">
                            <option value="">Select Region / क्षेत्र चुनें</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">🌱 Soil Type / मिट्टी:</label>
                        <select id="soil" class="w-full p-3 border border-gray-300 rounded-md" onchange="updateSoilInfo()">
                            <option value="">Select Soil / मिट्टी चुनें</option>
                        </select>
                    </div>
                    
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">📅 Sowing Month / बुआई महीना:</label>
                        <select id="month" class="w-full p-3 border border-gray-300 rounded-md">
                            <option value="">Select Month / महीना चुनें</option>
                            <option value="1">जनवरी / January</option>
                            <option value="2">फरवरी / February</option>
                            <option value="3">मार्च / March</option>
                            <option value="4">अप्रैल / April</option>
                            <option value="5">मई / May</option>
                            <option value="6">जून / June</option>
                            <option value="7">जुलाई / July</option>
                            <option value="8">अगस्त / August</option>
                            <option value="9">सितंबर / September</option>
                            <option value="10">अक्टूबर / October</option>
                            <option value="11">नवंबर / November</option>
                            <option value="12">दिसंबर / December</option>
                        </select>
                    </div>
                </div>
                
                <button onclick="getComprehensiveRecommendations()" class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition w-full md:w-auto">
                    🔍 Get Complete Analysis / पूर्ण विश्लेषण पाएं
                </button>
                
                <div id="recommendations" class="mt-6">
                    <div class="text-center text-gray-500 py-8">
                        <p>सभी जानकारी भरें और संपूर्ण कृषि विश्लेषण प्राप्त करें</p>
                        <p>Fill all details to get comprehensive agricultural analysis</p>
                    </div>
                </div>
            </div>
            
            <!-- Info Cards -->
            <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                <div id="region-info" class="bg-blue-50 border border-blue-200 rounded-lg p-4">
                    <h3 class="font-bold text-blue-800 mb-2">📍 Regional Climate Information</h3>
                    <p class="text-gray-600">Select region to see climate details</p>
                </div>
                
                <div id="soil-info" class="bg-yellow-50 border border-yellow-400 rounded-lg p-4">
                    <h3 class="font-bold text-yellow-800 mb-2">🌱 Soil Characteristics</h3>
                    <p class="text-gray-600">Select soil type to see detailed characteristics</p>
                </div>
            </div>
        </div>

        <!-- Yield Analysis Section -->
        <div id="yield" class="section hidden fade-in">
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-bold mb-4 text-green-800">📈 Detailed Yield Analysis & Harvest Planning</h2>
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Crop for Yield Analysis:</label>
                    <select id="yield-crop" class="w-full p-3 border border-gray-300 rounded-md">
                        <option value="">Choose Crop</option>
                    </select>
                </div>
                
                <button onclick="getYieldAnalysis()" class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
                    📊 Generate Yield Analysis
                </button>
                
                <div id="yield-results" class="mt-6"></div>
            </div>
        </div>

        <!-- Intercropping Section -->
        <div id="intercrop" class="section hidden fade-in">
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-bold mb-4 text-green-800">🌿 Advanced Intercropping & Pattern Planning</h2>
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Main Crop:</label>
                    <select id="intercrop-crop" class="w-full p-3 border border-gray-300 rounded-md">
                        <option value="">Choose Main Crop</option>
                    </select>
                </div>
                
                <button onclick="getIntercroppingAnalysis()" class="bg-purple-600 text-white px-6 py-3 rounded-lg hover:bg-purple-700 transition">
                    🌱 Get Intercropping Plan
                </button>
                
                <div id="intercrop-results" class="mt-6"></div>
            </div>
        </div>

        <!-- Crop Rotation Section -->
        <div id="rotation" class="section hidden fade-in">
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-bold mb-4 text-green-800">🔄 Smart Crop Rotation Planning</h2>
                
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-4 mb-6">
                    <h3 class="font-semibold text-blue-800 mb-2">📚 Crop Rotation Principles</h3>
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-4 text-sm">
                        <div class="space-y-2">
                            <p><strong>🚫 Family Rule:</strong> Avoid planting crops of the same family or vegetable in the same spot</p>
                            <p><strong>🌱 Root Depth:</strong> Alternate crops that feed near the surface with deep-rooting crops</p>
                            <p><strong>🔀 Crop Type:</strong> Follow root crops with vines or leaf crops</p>
                        </div>
                        <div class="space-y-2">
                            <p><strong>🌍 Soil Match:</strong> Choose crops that are suited to your soils</p>
                            <p><strong>🌾 Cover Crops:</strong> Use small grains or meadow to replace low residue crops for better erosion control</p>
                        </div>
                    </div>
                </div>
                
                <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-6">
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Select Current/Previous Crop:</label>
                        <select id="currentCrop" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500">
                            <option value="">Choose a crop...</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium text-gray-700 mb-2">Season for Next Crop:</label>
                        <select id="nextSeason" class="w-full px-3 py-2 border border-gray-300 rounded-md focus:outline-none focus:ring-2 focus:ring-green-500">
                            <option value="">Select season...</option>
                            <option value="Kharif">Kharif (Monsoon)</option>
                            <option value="Rabi">Rabi (Winter)</option>
                            <option value="Zaid">Zaid (Summer)</option>
                        </select>
                    </div>
                </div>
                
                <button onclick="getCropRotationPlan()" class="bg-green-600 text-white px-6 py-3 rounded-lg hover:bg-green-700 transition">
                    🔄 Get Rotation Plan
                </button>
                
                <div id="rotation-results" class="mt-6"></div>
            </div>
        </div>

        <!-- Maintenance Section -->
        <div id="maintenance" class="section hidden fade-in">
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-bold mb-4 text-green-800">🛠️ Complete Maintenance Schedule</h2>
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Select Crop for Maintenance Schedule:</label>
                    <select id="maintenance-crop" class="w-full p-3 border border-gray-300 rounded-md">
                        <option value="">Choose Crop</option>
                    </select>
                </div>
                
                <button onclick="getMaintenanceSchedule()" class="bg-orange-600 text-white px-6 py-3 rounded-lg hover:bg-orange-700 transition">
                    📅 Get Maintenance Schedule
                </button>
                
                <div id="maintenance-results" class="mt-6"></div>
            </div>
        </div>

        <!-- Weather Section -->
        <div id="weather" class="section hidden fade-in">
            <div class="bg-white rounded-lg shadow-md p-6">
                <h2 class="text-xl font-bold mb-4 text-green-800">🌤️ Real-Time Weather & Climate Analysis</h2>
                
                <div class="mb-4">
                    <label class="block text-sm font-medium text-gray-700 mb-2">Location:</label>
                    <input type="text" id="weather-location" placeholder="Udaipur, Rajasthan" 
                           class="w-full p-3 border border-gray-300 rounded-md">
                </div>
                
                <button onclick="getWeatherData()" class="bg-blue-600 text-white px-6 py-3 rounded-lg hover:bg-blue-700 transition">
                    🌡️ Get Weather Analysis
                </button>
                
                <div id="weather-results" class="mt-6"></div>
            </div>
        </div>

    </main>

    <footer class="bg-gray-800 text-white py-6 mt-12">
        <div class="container mx-auto px-4 text-center">
            <p>&copy; 2024 Uncompromized Smart Farmer Dashboard - Complete Agricultural Intelligence</p>
            <p class="text-gray-400 mt-2">🌾 {len(self.data['crops'])} Crops • Complete CSV Data Integration • Real-Time Analysis</p>
        </div>
    </footer>

    <script>
        let allData = {{}};

        // Initialize dashboard
        async function initDashboard() {{
            console.log('🌾 Initializing Ultimate Smart Farmer Dashboard...');
            await loadAllData();
            populateDropdowns();
        }}

        // Load all CSV data
        async function loadAllData() {{
            try {{
                const response = await fetch('/api/get-all-data');
                const data = await response.json();
                allData = data;
                console.log('✅ Complete data loaded:', {{
                    crops: allData.crops.length,
                    crop_yield: allData.crop_yield.length,
                    cropping_pattern: allData.cropping_pattern.length,
                    intercrops: allData.intercrops.length,
                    maintenance: allData.maintenance.length,
                    soil_types: allData.soil_types.length,
                    region_weather: allData.region_weather.length,
                    crop_suitability: allData.crop_suitability.length
                }});
            }} catch (error) {{
                console.error('❌ Error loading data:', error);
                showError('Data loading failed');
            }}
        }}

        // Populate dropdown menus
        function populateDropdowns() {{
            // Populate regions
            const regionSelect = document.getElementById('region');
            allData.region_weather.forEach(region => {{
                const option = document.createElement('option');
                option.value = region.region_id || region.id;
                option.textContent = `${{region.city_district}} (${{region.climate_zone}})`;
                regionSelect.appendChild(option);
            }});

            // Populate soil types
            const soilSelect = document.getElementById('soil');
            allData.soil_types.forEach(soil => {{
                const option = document.createElement('option');
                option.value = soil.soil_id || soil.id;
                option.textContent = `${{soil.name}} - ${{soil.color_origin}}`;
                soilSelect.appendChild(option);
            }});

            // Populate crop dropdowns
            const cropSelects = ['yield-crop', 'intercrop-crop', 'maintenance-crop', 'currentCrop'];
            cropSelects.forEach(selectId => {{
                const select = document.getElementById(selectId);
                if (select) {{
                    allData.crops.forEach(crop => {{
                        const option = document.createElement('option');
                        option.value = crop.CropID;
                        option.textContent = `${{crop.CropName}} (${{crop.CropType}})`;
                        select.appendChild(option);
                    }});
                }}
            }});
        }}

        // Update region info
        function updateRegionInfo() {{
            const regionId = document.getElementById('region').value;
            if (regionId) {{
                const region = allData.region_weather.find(r => (r.region_id || r.id) == regionId);
                if (region) {{
                    document.getElementById('region-info').innerHTML = `
                        <h3 class="font-bold text-blue-800 mb-2">📍 ${{region.city_district}}</h3>
                        <div class="grid grid-cols-2 gap-2 text-sm">
                            <p><strong>Climate Zone:</strong> ${{region.climate_zone}}</p>
                            <p><strong>Annual Rainfall:</strong> ${{region.ann_rain_mm || 'N/A'}}mm</p>
                            <p><strong>Temperature:</strong> ${{region.min_temp_c || 'N/A'}}°C - ${{region.max_temp_c || 'N/A'}}°C</p>
                            <p><strong>Humidity:</strong> ${{region.avg_humidity_percent || 'N/A'}}%</p>
                        </div>
                    `;
                }}
            }}
        }}

        // Update soil info
        function updateSoilInfo() {{
            const soilId = document.getElementById('soil').value;
            if (soilId) {{
                const soil = allData.soil_types.find(s => (s.soil_id || s.id) == soilId);
                if (soil) {{
                    document.getElementById('soil-info').innerHTML = `
                        <h3 class="font-bold text-yellow-800 mb-2">🌱 ${{soil.name}}</h3>
                        <div class="grid grid-cols-2 gap-2 text-sm">
                            <p><strong>Origin:</strong> ${{soil.color_origin}}</p>
                            <p><strong>Texture:</strong> ${{soil.texture_structure}}</p>
                            <p><strong>pH Range:</strong> ${{soil.min_ph}} - ${{soil.max_ph}}</p>
                            <p><strong>Water Retention:</strong> ${{soil.water_retention}}</p>
                            <p><strong>Fertility:</strong> ${{soil.fertility_level}}</p>
                        </div>
                    `;
                }}
            }}
        }}

        // Get comprehensive recommendations
        async function getComprehensiveRecommendations() {{
            const regionId = document.getElementById('region').value;
            const soilId = document.getElementById('soil').value;
            const month = document.getElementById('month').value;
            const resultsDiv = document.getElementById('recommendations');

            if (!regionId || !soilId || !month) {{
                showError('Please fill all fields / कृपया सभी फ़ील्ड भरें');
                return;
            }}

            resultsDiv.innerHTML = `
                <div class="text-center py-8">
                    <div class="loading mx-auto mb-4"></div>
                    <p class="text-blue-600">Analyzing complete agricultural data...</p>
                </div>
            `;

            try {{
                const response = await fetch('/api/comprehensive-recommendations', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{
                        region_id: regionId,
                        soil_id: soilId,
                        month: month
                    }})
                }});

                const data = await response.json();
                
                if (data.success && data.crops.length > 0) {{
                    displayComprehensiveRecommendations(data.crops);
                }} else {{
                    resultsDiv.innerHTML = `
                        <div class="text-center py-8 text-yellow-600">
                            <p>No suitable crops found for these conditions</p>
                            <p class="text-sm mt-2">Try different parameters</p>
                        </div>
                    `;
                }}
            }} catch (error) {{
                console.error('Error:', error);
                showError('Error getting recommendations');
            }}
        }}

        // Display comprehensive recommendations
        function displayComprehensiveRecommendations(crops) {{
            const resultsDiv = document.getElementById('recommendations');
            
            let html = '<div class="space-y-6">';
            
            crops.forEach(crop => {{
                const yieldInfo = crop.yield_info || {{}};
                const patternInfo = crop.pattern_info || {{}};
                const interInfo = crop.intercrop_info || {{}};
                const maintenanceCount = crop.total_maintenance_steps || 0;
                
                // Soil suitability badge color
                const suitabilityColor = crop.suitability_level === 'High' ? 'bg-green-500' : 
                                       crop.suitability_level === 'Very High' ? 'bg-emerald-600' : 'bg-yellow-500';
                
                html += `
                    <div class="border border-green-200 rounded-lg p-6 bg-green-50 shadow-md hover:shadow-lg transition-shadow">
                        <div class="flex justify-between items-start mb-4">
                            <div>
                                <h3 class="font-bold text-xl text-green-800">${{crop.CropName}}</h3>
                                <p class="text-gray-600">${{crop.CropFamily}} • ${{crop.CropType}} • ${{crop.Seasonality}}</p>
                                <p class="text-sm text-gray-500 mt-1">
                                    Sowing: ${{crop['Sowing Months']}} | Harvest: ${{crop['Harvesting Months']}}
                                </p>
                            </div>
                            <div class="text-right">
                                <span class="${{suitabilityColor}} text-white px-3 py-1 rounded text-sm font-semibold">
                                    ${{crop.suitability_level}} Suitability
                                </span>
                                <p class="text-xs text-gray-600 mt-1 max-w-48">${{crop.suitability_reason}}</p>
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 mb-4">
                            <div class="bg-white rounded-lg p-4 border-l-4 border-blue-500">
                                <h4 class="font-semibold text-blue-700 mb-2">🌱 Cultivation Details</h4>
                                <div class="space-y-1 text-sm">
                                    <p><strong>Duration:</strong> ${{crop.TypicalDuration_days}} days</p>
                                    <p><strong>Seed Rate:</strong> ${{crop.SeedRate_kg_per_ha}} kg/ha</p>
                                    <p><strong>Temperature:</strong> ${{crop.MinTemp_C}}-${{crop.MaxTemp_C}}°C</p>
                                    <p><strong>Irrigation:</strong> ${{crop.IrrigationRequirement_mm}}mm</p>
                                    <p><strong>Water Range:</strong> ${{crop['Water_Requirement_Min_(mm)']}}-${{crop['Water_Requirement_Max_(mm)']}}mm</p>
                                    <p><strong>Soil pH:</strong> ${{crop.MinSoilpH}}-${{crop.MaxSoilpH}}</p>
                                </div>
                            </div>
                            
                            <div class="bg-white rounded-lg p-4 border-l-4 border-purple-500">
                                <h4 class="font-semibold text-purple-700 mb-2">📈 Yield & Harvest</h4>
                                <div class="space-y-1 text-sm">
                                    <p><strong>Conv. Yield:</strong> ${{yieldInfo['Yield_Conv_Min_t'] || 'N/A'}}-${{yieldInfo['Yield_Conv_Max_t'] || 'N/A'}} t/ha</p>
                                    <p><strong>Organic Yield:</strong> ${{yieldInfo['Yield_Org Min (t)'] || 'N/A'}}-${{yieldInfo['Yield/Org Max (t)'] || 'N/A'}} t/ha</p>
                                    <p><strong>Plant Spacing:</strong> ${{yieldInfo['Spacing (cm x cm)'] || 'Standard'}}</p>
                                    <p><strong>Plants/Acre:</strong> ${{(yieldInfo.Plants_per_Acre || 'N/A').toLocaleString()}}</p>
                                    <p><strong>Harvest Method:</strong> ${{yieldInfo['Harvesting Method'] || 'Manual'}}</p>
                                    <p><strong>Harvest Freq:</strong> ${{yieldInfo['Harvesting Frequency'] || 'Single'}}</p>
                                </div>
                            </div>
                            
                            <div class="bg-white rounded-lg p-4 border-l-4 border-orange-500">
                                <h4 class="font-semibold text-orange-700 mb-2">🌿 Intercropping Plan</h4>
                                <div class="space-y-1 text-sm">
                                    <p><strong>Best Pattern:</strong> ${{patternInfo.Best_Cropping_Pattern || 'Monocropping'}}</p>
                                    <p><strong>Alt Pattern:</strong> ${{patternInfo.Second_Best_Pattern || 'N/A'}}</p>
                                    <p><strong>Top Intercrop:</strong> ${{interInfo.IntercropRank1 || 'None'}}</p>
                                    <p><strong>Rank 2:</strong> ${{interInfo.IntercropRank2 || 'N/A'}}</p>
                                    <p><strong>Rank 3:</strong> ${{interInfo.IntercropRank3 || 'N/A'}}</p>
                                    <p><strong>Key Benefits:</strong> ${{interInfo['Key Benefits'] || 'N/A'}}</p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-4 mb-4">
                            <div class="bg-white rounded-lg p-4 border-l-4 border-red-500">
                                <h4 class="font-semibold text-red-700 mb-2">🧪 Fertilizer & Nutrients</h4>
                                <div class="space-y-1 text-sm">
                                    <p><strong>Chemical Dose:</strong> ${{crop.FertilizerDose_kg_per_ha}}</p>
                                    <p><strong>Pesticides:</strong> ${{crop.PesticidesUsed}}</p>
                                    <p><strong>Required Nutrients:</strong> ${{crop['Nutrients Required']}}</p>
                                    <p><strong>Organic Alternatives:</strong></p>
                                    <p class="text-xs text-gray-600 mt-1">${{crop['Organic Fertilizer Substitutes']}}</p>
                                </div>
                            </div>
                            
                            <div class="bg-white rounded-lg p-4 border-l-4 border-green-500">
                                <h4 class="font-semibold text-green-700 mb-2">🛠️ Maintenance Overview</h4>
                                <div class="space-y-1 text-sm">
                                    <p><strong>Total Steps:</strong> ${{maintenanceCount}} detailed procedures</p>
                                    <p><strong>Labor Days:</strong> ${{crop.LabourDays_per_ha}}/ha</p>
                                    <p><strong>Manure Need:</strong> ${{crop.ManureRequirement_ton_per_ha}} ton/ha</p>
                                    <p><strong>Soil Types:</strong> ${{crop.SoilType}}</p>
                                    <p class="text-xs text-gray-600 mt-2">
                                        <strong>Reason for Soil Match:</strong> ${{crop.suitability_reason}}
                                    </p>
                                </div>
                            </div>
                        </div>
                        
                        <div class="flex flex-wrap gap-2">
                            <button onclick="getYieldAnalysisFor('${{crop.CropID}}')" 
                                    class="bg-blue-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-blue-600 transition-colors">
                                📊 Detailed Yield Analysis
                            </button>
                            <button onclick="getIntercroppingFor('${{crop.CropID}}')" 
                                    class="bg-purple-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-purple-600 transition-colors">
                                🌿 Intercropping Plan
                            </button>
                            <button onclick="getRotationPlanFor('${{crop.CropID}}')" 
                                    class="bg-green-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-green-600 transition-colors">
                                🔄 Rotation After This
                            </button>
                            <button onclick="getMaintenanceFor('${{crop.CropID}}')" 
                                    class="bg-orange-500 text-white px-4 py-2 rounded-lg text-sm hover:bg-orange-600 transition-colors">
                                🛠️ Full Maintenance (${{maintenanceCount}} steps)
                            </button>
                        </div>
                    </div>
                `;
            }});
            
            html += '</div>';
            resultsDiv.innerHTML = html;
        }}

        // Yield analysis functions
        function getYieldAnalysisFor(cropId) {{
            showSection('yield');
            document.getElementById('yield-crop').value = cropId;
            getYieldAnalysis();
        }}

        async function getYieldAnalysis() {{
            const cropId = document.getElementById('yield-crop').value;
            const resultsDiv = document.getElementById('yield-results');

            if (!cropId) {{
                resultsDiv.innerHTML = '<div class="text-red-600">Please select a crop</div>';
                return;
            }}

            const crop = allData.crops.find(c => c.CropID == cropId);
            const yieldInfo = allData.crop_yield.find(y => y.CropID == cropId);

            if (!crop || !yieldInfo) {{
                resultsDiv.innerHTML = '<div class="text-red-600">Crop data not found</div>';
                return;
            }}

            resultsDiv.innerHTML = `
                <div class="bg-blue-50 border border-blue-200 rounded-lg p-6">
                    <h3 class="font-bold text-blue-800 text-xl mb-4">📈 Complete Yield Analysis: ${{crop.CropName}}</h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div class="bg-white rounded-lg p-4">
                            <h4 class="font-bold text-green-700 mb-3">🌾 Yield Expectations</h4>
                            <p><strong>Conventional Yield:</strong> ${{yieldInfo['Yield_Conv_Min_t']}}-${{yieldInfo['Yield_Conv_Max_t']}} tons/ha</p>
                            <p><strong>Organic Yield:</strong> ${{yieldInfo['Yield_Org Min (t)']}}-${{yieldInfo['Yield/Org Max (t)']}} tons/ha</p>
                            <p><strong>Plant Spacing:</strong> ${{yieldInfo['Spacing (cm x cm)']}}</p>
                            <p><strong>Plants per Acre:</strong> ${{yieldInfo.Plants_per_Acre?.toLocaleString() || 'N/A'}}</p>
                            <p><strong>Main Harvest:</strong> ${{yieldInfo['Main Harvest Month(s)']}}</p>
                        </div>
                        
                        <div class="bg-white rounded-lg p-4">
                            <h4 class="font-bold text-purple-700 mb-3">📅 Harvest Schedule</h4>
                            <p><strong>Harvest Method:</strong> ${{yieldInfo['Harvest Method']}}</p>
                            <p><strong>Frequency:</strong> ${{yieldInfo['Harvest Frequency']}}</p>
                            <p><strong>Week 1 Yield:</strong> ${{yieldInfo['Wk 1 %']}}% (${{yieldInfo['Org Wk 1 Yield Min (t)']}}-${{yieldInfo['Org Wk 1 Yield Max (t)']}} t)</p>
                            <p><strong>Week 2 Yield:</strong> ${{yieldInfo['Wk 2 %']}}% (${{yieldInfo['Org Wk 2 Yield Min (t)']}}-${{yieldInfo['Org Wk 2 Yield Max (t)']}} t)</p>
                        </div>
                    </div>
                    
                    <div class="bg-white rounded-lg p-4">
                        <h4 class="font-bold text-orange-700 mb-3">📋 Harvest Details</h4>
                        <p class="text-sm">${{yieldInfo.Details}}</p>
                    </div>
                </div>
            `;
        }}

        // Intercropping functions
        function getIntercroppingFor(cropId) {{
            showSection('intercrop');
            document.getElementById('intercrop-crop').value = cropId;
            getIntercroppingAnalysis();
        }}

        async function getIntercroppingAnalysis() {{
            const cropId = document.getElementById('intercrop-crop').value;
            const resultsDiv = document.getElementById('intercrop-results');

            if (!cropId) {{
                resultsDiv.innerHTML = '<div class="text-red-600">Please select a crop</div>';
                return;
            }}

            const crop = allData.crops.find(c => c.CropID == cropId);
            const patternInfo = allData.cropping_pattern.find(p => p.CropID == cropId);
            const interInfo = allData.intercrops.find(i => i.CropID == cropId);

            resultsDiv.innerHTML = `
                <div class="bg-purple-50 border border-purple-200 rounded-lg p-6">
                    <h3 class="font-bold text-purple-800 text-xl mb-4">🌿 Intercropping Plan: ${{crop.CropName}}</h3>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6 mb-6">
                        <div class="bg-white rounded-lg p-4">
                            <h4 class="font-bold text-green-700 mb-3">🔄 Cropping Patterns</h4>
                            <p><strong>Best Pattern:</strong> ${{patternInfo?.Best_Cropping_Pattern || 'Monocropping'}}</p>
                            <p><strong>Second Best:</strong> ${{patternInfo?.Second_Best_Pattern || 'N/A'}}</p>
                            <p><strong>Reason:</strong> ${{patternInfo?.Reason || 'Standard cultivation'}}</p>
                        </div>
                        
                        <div class="bg-white rounded-lg p-4">
                            <h4 class="font-bold text-blue-700 mb-3">🌱 Intercrop Options</h4>
                            <p><strong>Rank 1:</strong> ${{interInfo?.IntercropRank1 || 'N/A'}}</p>
                            <p><strong>Rank 2:</strong> ${{interInfo?.IntercropRank2 || 'N/A'}}</p>
                            <p><strong>Rank 3:</strong> ${{interInfo?.IntercropRank3 || 'N/A'}}</p>
                        </div>
                    </div>
                    
                    <div class="grid grid-cols-1 md:grid-cols-2 gap-6">
                        <div class="bg-white rounded-lg p-4">
                            <h4 class="font-bold text-orange-700 mb-3">✅ Key Benefits</h4>
                            <p>${{interInfo?.KeyBenefits || 'Improved land use efficiency'}}</p>
                        </div>
                        
                        <div class="bg-white rounded-lg p-4">
                            <h4 class="font-bold text-red-700 mb-3">🛡️ Pest Management</h4>
                            <p>${{interInfo?.PestDiseaseManagement || 'Standard pest control measures'}}</p>
                        </div>
                    </div>
                </div>
            `;
        }}

        // Maintenance functions
        function getMaintenanceFor(cropId) {{
            showSection('maintenance');
            document.getElementById('maintenance-crop').value = cropId;
            getMaintenanceSchedule();
        }}

        async function getMaintenanceSchedule() {{
            const cropId = document.getElementById('maintenance-crop').value;
            const resultsDiv = document.getElementById('maintenance-results');

            if (!cropId) {{
                resultsDiv.innerHTML = '<div class="text-red-600">Please select a crop</div>';
                return;
            }}

            try {{
                const response = await fetch('/api/maintenance-schedule', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ crop_id: cropId }})
                }});

                const data = await response.json();
                
                if (data.success && data.schedule.length > 0) {{
                    displayMaintenanceSchedule(data.schedule, data.crop_name);
                }} else {{
                    resultsDiv.innerHTML = '<div class="text-yellow-600">No maintenance schedule found for this crop</div>';
                }}
            }} catch (error) {{
                resultsDiv.innerHTML = '<div class="text-red-600">Error loading maintenance schedule</div>';
            }}
        }}

        function displayMaintenanceSchedule(schedule, cropName) {{
            const resultsDiv = document.getElementById('maintenance-results');
            
            let html = `
                <div class="bg-orange-50 border border-orange-200 rounded-lg p-6">
                    <h3 class="font-bold text-orange-800 text-xl mb-4">🛠️ Complete Maintenance Schedule: ${{cropName}}</h3>
                    <div class="space-y-4">
            `;
            
            schedule.forEach(step => {{
                html += `
                    <div class="bg-white rounded-lg p-4 border border-gray-200">
                        <h4 class="font-bold text-gray-800 mb-2">${{step.Maintenance_Step}}</h4>
                        <div class="grid grid-cols-1 md:grid-cols-3 gap-4 text-sm">
                            <div>
                                <strong>Timing:</strong> ${{step.TimingandStage}}
                            </div>
                            <div>
                                <strong>Irrigation:</strong> ${{step.Irrigation_Schedule}}
                            </div>
                            <div>
                                <strong>Fertilizer:</strong> ${{step.Organic_Fertilizer_Schedule}}
                            </div>
                        </div>
                        <div class="mt-2 text-sm">
                            <strong>Pest Management:</strong> ${{step.Pest_Management}}
                        </div>
                    </div>
                `;
            }});
            
            html += '</div></div>';
            resultsDiv.innerHTML = html;
        }}

        function getRotationPlanFor(cropId) {{
            // Set the current crop in rotation section and switch to it
            document.getElementById('currentCrop').value = cropId;
            document.getElementById('nextSeason').value = 'Rabi'; // Default to Rabi
            showSection('rotation');
            
            // Scroll to rotation section
            setTimeout(() => {{
                document.getElementById('rotation').scrollIntoView({{ behavior: 'smooth' }});
            }}, 100);
        }}

        // Crop Rotation functions
        async function getCropRotationPlan() {{
            const currentCropId = document.getElementById('currentCrop').value;
            const nextSeason = document.getElementById('nextSeason').value;
            const resultsDiv = document.getElementById('rotation-results');

            if (!currentCropId || !nextSeason) {{
                resultsDiv.innerHTML = '<div class="text-red-600">Please select both current crop and next season</div>';
                return;
            }}

            try {{
                const response = await fetch('/api/crop-rotation', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ current_crop_id: currentCropId, next_season: nextSeason }})
                }});

                const data = await response.json();
                
                if (data.success) {{
                    displayRotationPlan(data.current_crop, data.recommended_crops, data.rotation_rules);
                }} else {{
                    resultsDiv.innerHTML = '<div class="text-red-600">Error getting rotation plan</div>';
                }}
            }} catch (error) {{
                resultsDiv.innerHTML = '<div class="text-red-600">Network error getting rotation plan</div>';
            }}
        }}

        function displayRotationPlan(currentCrop, recommendedCrops, rules) {{
            const resultsDiv = document.getElementById('rotation-results');
            
            let html = `
                <div class="bg-gray-50 rounded-lg p-6">
                    <h3 class="font-bold text-green-800 text-xl mb-4">🔄 Rotation Plan After: ${{currentCrop.CropName}}</h3>
                    
                    <div class="mb-6">
                        <h4 class="font-semibold text-gray-700 mb-3">📋 Rotation Rules Applied:</h4>
                        <div class="grid grid-cols-1 md:grid-cols-2 gap-2">
            `;
            
            rules.forEach(rule => {{
                html += `<div class="bg-blue-100 border border-blue-200 rounded p-2 text-sm">✓ ${{rule}}</div>`;
            }});
            
            html += `
                        </div>
                    </div>
                    
                    <h4 class="font-semibold text-green-700 mb-4">🌱 Recommended Next Crops:</h4>
                    <div class="grid grid-cols-1 md:grid-cols-2 lg:grid-cols-3 gap-4">
            `;

            recommendedCrops.forEach(crop => {{
                const suitabilityColor = crop.rotation_score >= 8 ? 'bg-green-500' : 
                                       crop.rotation_score >= 6 ? 'bg-yellow-500' : 'bg-orange-500';
                
                html += `
                    <div class="border border-gray-200 rounded-lg p-4 bg-white shadow hover:shadow-md transition-shadow">
                        <div class="flex justify-between items-start mb-3">
                            <h5 class="font-bold text-gray-800">${{crop.CropName}}</h5>
                            <span class="${{suitabilityColor}} text-white px-2 py-1 rounded text-xs font-semibold">
                                ${{crop.rotation_score}}/10
                            </span>
                        </div>
                        <p class="text-sm text-gray-600 mb-2">${{crop.CropFamily}} • ${{crop.Seasonality}}</p>
                        <p class="text-xs text-green-700 mb-2"><strong>Sowing:</strong> ${{crop['Sowing Months']}}</p>
                        <p class="text-xs text-gray-600"><strong>Why good:</strong> ${{crop.rotation_reason}}</p>
                        <div class="mt-3 flex flex-wrap gap-1">
                            <span class="bg-blue-100 text-blue-800 px-2 py-1 rounded text-xs">${{crop.CropType}}</span>
                            <span class="bg-purple-100 text-purple-800 px-2 py-1 rounded text-xs">pH: ${{crop.MinSoilpH}}-${{crop.MaxSoilpH}}</span>
                        </div>
                    </div>
                `;
            }});
            
            html += `
                    </div>
                    
                    <div class="mt-6 bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                        <h4 class="font-semibold text-yellow-800 mb-2">💡 Rotation Tips:</h4>
                        <ul class="text-sm text-yellow-700 space-y-1">
                            <li>• Different plant families help break pest and disease cycles</li>
                            <li>• Legumes fix nitrogen, benefiting subsequent crops</li>
                            <li>• Deep-rooted crops improve soil structure for shallow-rooted ones</li>
                            <li>• Rotation maintains soil fertility and reduces input costs</li>
                        </ul>
                    </div>
                </div>
            `;
            
            resultsDiv.innerHTML = html;
        }}

        // Weather functions
        async function getWeatherData() {{
            const location = document.getElementById('weather-location').value;
            const resultsDiv = document.getElementById('weather-results');

            if (!location) {{
                resultsDiv.innerHTML = '<div class="text-red-600">Please enter location</div>';
                return;
            }}

            resultsDiv.innerHTML = `
                <div class="text-center py-4">
                    <div class="loading mx-auto mb-4"></div>
                    <p class="text-blue-600">Getting weather data...</p>
                </div>
            `;

            try {{
                const response = await fetch('/api/weather', {{
                    method: 'POST',
                    headers: {{ 'Content-Type': 'application/json' }},
                    body: JSON.stringify({{ location: location }})
                }});

                const data = await response.json();
                
                if (data.success) {{
                    resultsDiv.innerHTML = `
                        <div class="weather-card text-white rounded-lg p-6">
                            <h3 class="text-xl font-bold mb-4">🌤️ ${{location}} Weather</h3>
                            <div class="grid grid-cols-2 md:grid-cols-4 gap-4">
                                <div class="text-center">
                                    <p class="text-3xl font-bold">${{data.temperature}}°C</p>
                                    <p class="text-sm opacity-80">Temperature</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-3xl font-bold">${{data.humidity}}%</p>
                                    <p class="text-sm opacity-80">Humidity</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-3xl font-bold">${{data.precipitation}}</p>
                                    <p class="text-sm opacity-80">Precipitation</p>
                                </div>
                                <div class="text-center">
                                    <p class="text-3xl font-bold">${{data.windspeed}}</p>
                                    <p class="text-sm opacity-80">Wind Speed</p>
                                </div>
                            </div>
                            <div class="mt-4 text-center">
                                <p class="text-lg">${{data.conditions}}</p>
                                <p class="text-sm opacity-80">Current Conditions</p>
                            </div>
                        </div>
                    `;
                }} else {{
                    resultsDiv.innerHTML = `
                        <div class="bg-yellow-50 border border-yellow-200 rounded-lg p-4">
                            <p class="text-yellow-800">Could not get weather data</p>
                            <p class="text-sm text-yellow-600 mt-2">Error: ${{data.error}}</p>
                        </div>
                    `;
                }}
            }} catch (error) {{
                resultsDiv.innerHTML = `
                    <div class="bg-red-50 border border-red-200 rounded-lg p-4">
                        <p class="text-red-800">Weather service error</p>
                    </div>
                `;
            }}
        }}

        // Utility functions
        function showSection(sectionName) {{
            document.querySelectorAll('.section').forEach(section => {{
                section.classList.add('hidden');
            }});
            document.getElementById(sectionName).classList.remove('hidden');
            
            document.querySelectorAll('.nav-btn').forEach(btn => {{
                btn.classList.remove('bg-green-500', 'text-white');
                btn.classList.add('bg-gray-200', 'text-gray-700');
            }});
            event.target.classList.remove('bg-gray-200', 'text-gray-700');
            event.target.classList.add('bg-green-500', 'text-white');
        }}

        function showError(message) {{
            const resultsDiv = document.getElementById('recommendations');
            resultsDiv.innerHTML = `
                <div class="bg-red-50 border border-red-200 rounded-lg p-4 text-center">
                    <p class="text-red-600">${{message}}</p>
                </div>
            `;
        }}

        // Initialize on page load
        document.addEventListener('DOMContentLoaded', initDashboard);
    </script>
</body>
</html>
        """

        self.send_response(200)
        self.send_header('Content-type', 'text/html')
        self.end_headers()
        self.wfile.write(html_content.encode('utf-8'))

    def handle_api_request(self):
        """Handle API requests"""
        path = self.path.split('?')[0]
        
        if path == '/api/get-all-data':
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            self.wfile.write(json.dumps(self.data, ensure_ascii=False).encode('utf-8'))
        
        elif path == '/api/comprehensive-recommendations':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            crops = self.find_suitable_crops(
                request_data.get('region_id'),
                request_data.get('soil_id'),
                request_data.get('month')
            )
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'success': True,
                'crops': crops[:15]  # Top 15 comprehensive results
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif path == '/api/maintenance-schedule':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            crop_id = request_data.get('crop_id')
            schedule = self.get_maintenance_schedule(crop_id)
            crop = next((c for c in self.data['crops'] if str(c.get('CropID', '')) == str(crop_id)), {})
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            response = {
                'success': True,
                'schedule': schedule,
                'crop_name': crop.get('CropName', 'Unknown Crop')
            }
            
            self.wfile.write(json.dumps(response, ensure_ascii=False).encode('utf-8'))
        
        elif path == '/api/weather':
            content_length = int(self.headers['Content-Length'])
            post_data = self.rfile.read(content_length)
            request_data = json.loads(post_data.decode('utf-8'))
            
            weather_data = self.get_weather_data(request_data.get('location', ''))
            
            self.send_response(200)
            self.send_header('Content-type', 'application/json')
            self.end_headers()
            
            self.wfile.write(json.dumps(weather_data, ensure_ascii=False).encode('utf-8'))
        
        elif self.path == '/api/crop-rotation':
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length).decode('utf-8') if content_length > 0 else '{}'
            
            try:
                data = json.loads(body) if body.strip() else {}
                current_crop_id = str(data.get('current_crop_id', ''))
                next_season = data.get('next_season', '')
                
                if not current_crop_id or not next_season:
                    self.send_response(400)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Missing parameters'}).encode())
                    return

                # Get current crop info
                current_crop = next((c for c in self.data['crops'] if str(c.get('CropID', '')) == current_crop_id), {})
                if not current_crop:
                    self.send_response(404)
                    self.send_header('Content-type', 'application/json')
                    self.end_headers()
                    self.wfile.write(json.dumps({'success': False, 'error': 'Crop not found'}).encode())
                    return

                # Get recommended rotation crops
                recommended_crops = self.get_rotation_recommendations(current_crop, next_season)
                rotation_rules = [
                    "Avoid planting crops of the same family in sequence",
                    "Alternate surface-feeding with deep-rooting crops", 
                    "Follow root crops with vines or leaf crops",
                    "Choose crops suited to your soil type and pH",
                    "Use legumes to naturally fix nitrogen in soil"
                ]

                self.send_response(200)
                self.send_header('Content-type', 'application/json')
                self.send_header('Access-Control-Allow-Origin', '*')
                self.end_headers()
                
                response_data = {
                    'success': True,
                    'current_crop': current_crop,
                    'recommended_crops': recommended_crops,
                    'rotation_rules': rotation_rules
                }
                
                self.wfile.write(json.dumps(response_data, ensure_ascii=False).encode('utf-8'))

            except Exception as e:
                self.send_response(500)
                self.send_header('Content-type', 'application/json')
                self.end_headers()
                self.wfile.write(json.dumps({'success': False, 'error': str(e)}).encode())
        
        else:
            self.send_response(404)
            self.end_headers()

    def get_rotation_recommendations(self, current_crop, next_season):
        """Get crop rotation recommendations based on rotation principles"""
        recommendations = []
        current_family = current_crop.get('CropFamily', '').lower()
        current_type = current_crop.get('CropType', '').lower()
        
        for crop in self.data['crops']:
            if str(crop.get('CropID', '')) == str(current_crop.get('CropID', '')):
                continue  # Skip same crop
            
            if crop.get('Seasonality', '').lower() != next_season.lower():
                continue  # Skip wrong season
            
            score = 5  # Base score
            reasons = []
            
            # Rule 1: Different family bonus
            if crop.get('CropFamily', '').lower() != current_family:
                score += 2
                reasons.append(f"Different family ({crop.get('CropFamily', '')} vs {current_crop.get('CropFamily', '')})")
            else:
                score -= 1
                reasons.append("Same family - not ideal for rotation")
            
            # Rule 2: Different crop type bonus  
            if crop.get('CropType', '').lower() != current_type:
                score += 1
                reasons.append(f"Different type ({crop.get('CropType', '')} vs {current_crop.get('CropType', '')})")
            
            # Rule 3: Legume after non-legume bonus
            if 'legume' in crop.get('CropFamily', '').lower() and 'legume' not in current_family:
                score += 2
                reasons.append("Legume crop will fix nitrogen for soil")
            
            # Rule 4: Deep vs shallow rooted
            deep_rooted = ['mustard', 'safflower', 'sunflower', 'cotton']
            shallow_rooted = ['rice', 'wheat', 'barley']
            current_name = current_crop.get('CropName', '').lower()
            crop_name = crop.get('CropName', '').lower()
            
            if any(deep in current_name for deep in deep_rooted) and any(shallow in crop_name for shallow in shallow_rooted):
                score += 1
                reasons.append("Shallow roots after deep-rooted crop")
            elif any(shallow in current_name for shallow in shallow_rooted) and any(deep in crop_name for deep in deep_rooted):
                score += 1
                reasons.append("Deep roots after shallow-rooted crop")
            
            # Rule 5: Soil pH compatibility
            try:
                current_min_ph = float(current_crop.get('MinSoilpH', 6.0))
                current_max_ph = float(current_crop.get('MaxSoilpH', 7.5))
                crop_min_ph = float(crop.get('MinSoilpH', 6.0))
                crop_max_ph = float(crop.get('MaxSoilpH', 7.5))
                
                # Check pH overlap
                if (crop_min_ph <= current_max_ph and crop_max_ph >= current_min_ph):
                    score += 1
                    reasons.append("Compatible soil pH requirements")
            except:
                pass
            
            # Cap the score at 10
            score = min(score, 10)
            
            crop_copy = crop.copy()
            crop_copy['rotation_score'] = score
            crop_copy['rotation_reason'] = '; '.join(reasons[:2])  # Top 2 reasons
            
            recommendations.append(crop_copy)
        
        # Sort by score (highest first)
        recommendations.sort(key=lambda x: x['rotation_score'], reverse=True)
        return recommendations[:6]  # Return top 6 recommendations

def find_free_port():
    """Find a free port starting from 8000"""
    for port in range(8000, 8010):
        try:
            with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
                s.bind(('', port))
                return port
        except OSError:
            continue
    return None
    return None

def main():
    """Start the Ultimate Smart Farmer Dashboard"""
    PORT = find_free_port()
    
    if PORT is None:
        print("❌ No free ports found in range 8000-8009")
        print("Please close other applications and try again")
        input("Press Enter to exit...")
        return
    
    # Change to the correct directory
    os.chdir(os.path.dirname(os.path.abspath(__file__)))
    
    print("🌾 UNCOMPROMIZED SMART FARMER DASHBOARD")
    print("=" * 80)
    print(f"🌐 Dashboard URL: http://localhost:{PORT}")
    print("\n📊 COMPLETE CSV DATA INTEGRATION:")
    print("   ✅ crops.csv - 57+ crops with full agricultural data")
    print("   ✅ crop_yield.csv - Detailed yield and harvest information")
    print("   ✅ cropping_pattern.csv - Intercropping and rotation patterns")
    print("   ✅ intercrops.csv - Detailed intercropping combinations")
    print("   ✅ maintenance.csv - Complete maintenance schedules")
    print("   ✅ soil_types.csv - Comprehensive soil characteristics")
    print("   ✅ region_weather.csv - Regional climate data")
    print("   ✅ crop_suitability.csv - Crop-soil matching database")
    print("\n🚀 FEATURES:")
    print("   📈 Complete yield analysis with harvest schedules")
    print("   🌿 Advanced intercropping and pattern planning")
    print("   🛠️ Detailed maintenance schedules for every crop")
    print("   🌤️ Real-time weather integration")
    print("   📱 Mobile-friendly responsive design")
    print("   🌍 Hindi + English bilingual interface")
    print("\n🚀 Starting server...")
    
    try:
        with socketserver.TCPServer(("", PORT), UltimateSmartFarmerHandler) as httpd:
            print(f"✅ Server started successfully on port {PORT}!")
            print(f"🌐 Open: http://localhost:{PORT}")
            print("🛑 Press Ctrl+C to stop")
            
            # Open browser automatically
            try:
                webbrowser.open(f'http://localhost:{PORT}')
                print("🚀 Browser opened automatically")
            except:
                print("⚠️  Please manually open the URL in your browser")
            
            print("=" * 80)
            httpd.serve_forever()
            
    except Exception as e:
        print(f"❌ Error starting server: {e}")
        input("Press Enter to exit...")

if __name__ == "__main__":
    main()
