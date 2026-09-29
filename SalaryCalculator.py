
# Employee Profile
EMPLOYEE_NAME = "Olatoye Toyeeb"

# Application Header
print("=" * 60)
print(f"      PORTAL ACCESS: payroll_sys_{EMPLOYEE_NAME.lower().replace(' ', '_')}")
print("=" * 60)
print(f" Welcome back, {EMPLOYEE_NAME}.\n Please input the financial details below:")
print("-" * 60)

# Input parameters
hourly_rate = float(input("   ▸ Enter Hourly Rate (₦): "))
hours_worked = float(input("   ▸ Enter Total Hours Worked: "))

# Financial computations
gross_salary = hourly_rate * hours_worked
tax_deduction = gross_salary * 0.05  # Standard 5% basic withholding tax
net_salary = gross_salary - tax_deduction

# Render Earnings Summary Slip
print("\n" + "=" * 60)
print(f"                EARNINGS SUMMARY STATEMENT                 ")
print("=" * 60)
print(f"  Employee Name     :  {EMPLOYEE_NAME}")
print(f"  Rate Per Hour     :  ₦{hourly_rate:,.2f} / hr")
print(f"  Hours Rendered    :  {hours_worked:,.1f} hrs")
print("-" * 60)
print(f"  Gross Earnings    :  ₦{gross_salary:,.2f}")
print(f"  Tax Deducted (5%) : -₦{tax_deduction:,.2f}")
print("-" * 60)
print(f"  NET TAKE-HOME PAY :  ₦{net_salary:,.2f}")
print("=" * 60)
print("  Status: PROCESSED & READY FOR DISBURSEMENT")
print("=" * 60)
