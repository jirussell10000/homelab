
import argparse
import math
import sys

# Constants
G_IMPERIAL = 32.174  # ft/s^2

def calculate_reynolds(v, D, nu):
    """
    Calculate Reynolds number.
    v: Velocity (ft/s)
    D: Diameter (ft)
    nu: Kinematic Viscosity (ft^2/s)
    """
    if nu == 0:
        return float('inf')
    return (v * D) / nu

def colebrook_white(Re, epsilon, D):
    """
    Calculate friction factor f using Colebrook-White equation.
    Re: Reynolds number
    epsilon: Roughness (ft)
    D: Diameter (ft)
    
    1/sqrt(f) = -2 * log10( (epsilon/D)/3.7 + 2.51/(Re * sqrt(f)) )
    """
    if Re < 2000:
        return 64 / Re  # Laminar flow
    
    # Initial guess for f (Newton-Raphson or simple iteration)
    # Using Swamee-Jain for a good initial guess
    if Re < 4000:
       # Critical zone approximation, just use a starting point
       f_guess = 0.02
    else:
        f_guess = 0.25 / (math.log10((epsilon / D) / 3.7 + 5.74 / (Re ** 0.9))) ** 2

    # Newton-Raphson iteration for better precision
    f = f_guess
    for _ in range(20): # Max 20 iterations
        if f <= 0: f = 0.0001 # Prevent math domain error
        sqrt_f = math.sqrt(f)
        term1 = (epsilon / D) / 3.7
        term2 = 2.51 / (Re * sqrt_f)
        
        g_val = -2.0 * math.log10(term1 + term2) - 1.0/sqrt_f
        
        # Derivative dg/df
        # dg/df = (-2 / ln(10)) * (1 / (term1 + term2)) * (2.51 / Re) * (-0.5 * f^(-1.5)) - (-0.5 * f^(-1.5))
        # This derivative is complex, let's use simple fixed-point iteration instead if Newton is too complex to implement quickly without error.
        # Actually, simple fixed point is often employed for Colebrook:
        # 1/sqrt(f_new) = -2 * log10(...)
        
        inv_sqrt_f_new = -2.0 * math.log10(term1 + term2)
        f_new = (1.0 / inv_sqrt_f_new) ** 2
        
        if abs(f_new - f) < 1e-6:
            return f_new
        f = f_new
        
    return f

def solve_velocity(mu, rho, epsilon, h_f, L, D):
    """
    Solve for velocity given Diameter.
    mu: Absolute Viscosity (lb*s/ft^2)
    rho: Density (slugs/ft^3)
    epsilon: Roughness (ft)
    h_f: Head Loss (ft)
    L: Length (ft)
    D: Diameter (ft)
    """
    nu = mu / rho # Kinematic viscosity
    
    # Initial guess for f
    f = 0.02 
    
    print(f"\n{'Iteration':<10} {'f':<10} {'Velocity (ft/s)':<20} {'Reynolds':<15}")
    print("-" * 60)
    
    for i in range(100):
        # Darcy-Weisbach: h_f = f * (L/D) * (v^2 / 2g)
        # => v = sqrt( (h_f * 2g * D) / (f * L) )
        try:
            v = math.sqrt((h_f * 2 * G_IMPERIAL * D) / (f * L))
        except ValueError:
            print("Error: Invalid inputs resulting in negative root (check units).")
            return None

        Re = calculate_reynolds(v, D, nu)
        f_new = colebrook_white(Re, epsilon, D)
        
        print(f"{i+1:<10} {f:.6f}   {v:.6f}             {Re:.2e}")
        
        if abs(f_new - f) < 1e-6:
            print("-" * 60)
            print(f"Converged in {i+1} iterations.")
            return v
        
        f = f_new
        
    print("Did not converge.")
    return None

def solve_diameter(mu, rho, epsilon, h_f, L, v):
    """
    Solve for diameter given Velocity.
    mu: Absolute Viscosity (lb*s/ft^2)
    rho: Density (slugs/ft^3)
    epsilon: Roughness (ft)
    h_f: Head Loss (ft)
    L: Length (ft)
    v: Velocity (ft/s)
    """
    nu = mu / rho
    
    # Initial guess for f
    f = 0.02
    
    print(f"{'Iteration':<10} {'f':<10} {'Diameter (ft)':<20} {'Reynolds':<15}")
    print("-" * 60)
    
    for i in range(100):
        # Darcy-Weisbach: h_f = f * (L/D) * (v^2 / 2g)
        # => D = (f * L * v^2) / (h_f * 2g)
        D = (f * L * v**2) / (h_f * 2 * G_IMPERIAL)
        
        Re = calculate_reynolds(v, D, nu)
        f_new = colebrook_white(Re, epsilon, D)
        
        print(f"{i+1:<10} {f:.6f}   {D:.6f}             {Re:.2e}")
        
        if abs(f_new - f) < 1e-6:
            print("-" * 60)
            print(f"Converged in {i+1} iterations.")
            return D
            
        f = f_new

    print("Did not converge.")
    return None

def main():
    parser = argparse.ArgumentParser(description="Darcy-Weisbach Solver (Imperial Units)")
    
    # Common arguments
    parser.add_argument("--mu", type=float, required=True, help="Absolute Viscosity (lb*s/ft^2)")
    parser.add_argument("--rho", type=float, required=True, help="Density (slugs/ft^3)")
    parser.add_argument("--epsilon", type=float, required=True, help="Pipe Roughness (ft)")
    parser.add_argument("--hf", type=float, required=True, help="Head Loss (ft)")
    parser.add_argument("--L", type=float, required=True, help="Pipe Length (ft)")
    
    # Mutually exclusive group for what to solve for
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument("--solve-v", action="store_true", help="Solve for velocity (requires --D)")
    group.add_argument("--solve-d", action="store_true", help="Solve for diameter (requires --v)")
    
    parser.add_argument("--D", type=float, help="Diameter (ft) - required if solving for velocity")
    parser.add_argument("--v", type=float, help="Velocity (ft/s) - required if solving for diameter")

    args = parser.parse_args()

    # Input validation logic
    if args.solve_v and args.D is None:
        parser.error("--D is required when solving for velocity.")
    if args.solve_d and args.v is None:
        parser.error("--v is required when solving for diameter.")

    if args.solve_v:
        result = solve_velocity(args.mu, args.rho, args.epsilon, args.hf, args.L, args.D)
        if result:
            print(f"\nCalculated Velocity: {result:.4f} ft/s")
    
    elif args.solve_d:
        result = solve_diameter(args.mu, args.rho, args.epsilon, args.hf, args.L, args.v)
        if result:
            print(f"\nCalculated Diameter: {result:.4f} ft")

if __name__ == "__main__":
    main()
