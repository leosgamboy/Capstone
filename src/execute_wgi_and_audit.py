#!/usr/bin/env python3
"""
Execute WGI integration and comprehensive data audit
"""

import sys
import os
sys.path.append(os.path.dirname(os.path.abspath(__file__)))

def main():
    """Execute WGI integration and audit"""
    print("🚀 EXECUTING WGI INTEGRATION AND COMPREHENSIVE AUDIT")
    print("="*80)
    
    # Step 1: Run WGI Integration
    print("\n📊 STEP 1: Running WGI Integration...")
    try:
        from comprehensive_wgi_integration import ComprehensiveWGIIntegrator
        
        integrator = ComprehensiveWGIIntegrator()
        
        # Load and process WGI data
        wgi_annual = integrator.load_and_process_wgi()
        if wgi_annual is None:
            print("❌ Failed to process WGI data")
            return
        
        # Create monthly WGI panel
        wgi_monthly = integrator.create_monthly_wgi_panel(wgi_annual)
        if wgi_monthly is None:
            print("❌ Failed to create monthly WGI panel")
            return
        
        # Load existing data
        bond_data, macro_data = integrator.load_existing_data()
        
        # Integrate all data
        merged_data = integrator.integrate_all_data(bond_data, wgi_monthly, macro_data)
        if merged_data is None:
            print("❌ Failed to integrate data")
            return
        
        # Filter and save final dataset
        output_file = integrator.filter_and_save(merged_data)
        
        print(f"\n✅ WGI Integration completed! Output: {output_file}")
        
    except Exception as e:
        print(f"❌ WGI Integration failed: {e}")
        return
    
    # Step 2: Run Comprehensive Data Audit
    print("\n📊 STEP 2: Running Comprehensive Data Audit...")
    try:
        from comprehensive_data_audit import ComprehensiveDataAuditor
        
        auditor = ComprehensiveDataAuditor()
        summary = auditor.create_comprehensive_summary()
        
        print("\n✅ Comprehensive Data Audit completed!")
        
    except Exception as e:
        print(f"❌ Data Audit failed: {e}")
        return
    
    print("\n" + "="*80)
    print("🎯 FINAL SUMMARY")
    print("="*80)
    print("✅ WGI Integration: COMPLETED")
    print("✅ Data Audit: COMPLETED")
    print("📁 Final Dataset: data/merged_panel_with_wgi.csv")
    print("📊 Ready for Double ML Analysis!")

if __name__ == "__main__":
    main() 