"""
Example: Compute on Encrypted Data
Demonstrates FHE operations - computing on encrypted data without decryption.
"""

from crypto.fhe_engine import FHEEngine
from rich.console import Console
from rich.table import Table

console = Console()


def demo_encrypted_statistics():
    """
    Demonstrate computing statistics on encrypted data.
    This is the core of Fully Homomorphic Encryption!
    """
    console.print("\n[bold blue]🔬 Encrypted Statistics Demo[/bold blue]\n")
    
    # Initialize FHE
    fhe = FHEEngine()
    if not fhe.load_context():
        console.print("[yellow]Creating FHE context...[/yellow]")
        fhe.setup(scheme="ckks")
    
    # Sample data - imagine this is sensitive code metrics
    console.print("[cyan]Scenario: Computing code complexity metrics (encrypted)[/cyan]\n")
    
    complexity_scores = [2.5, 3.7, 1.8, 4.2, 2.9, 3.1, 2.6, 3.8, 2.2, 4.0]
    console.print(f"📊 Complexity Scores: {complexity_scores}")
    
    # Encrypt data
    console.print("\n🔐 [yellow]Encrypting data...[/yellow]")
    encrypted_scores = fhe.encrypt(complexity_scores)
    console.print("✅ Data encrypted\n")
    
    # Compute statistics on ENCRYPTED data
    console.print("🔬 [yellow]Computing on encrypted data...[/yellow]")
    console.print("   (Data is NEVER decrypted during computation!)\n")
    
    # Sum
    console.print("1️⃣  Computing sum...")
    enc_sum = fhe.sum_encrypted(encrypted_scores)
    
    # Mean
    console.print("2️⃣  Computing mean...")
    enc_mean = fhe.mean_encrypted(encrypted_scores)
    
    # Decrypt results only at the end
    console.print("\n🔓 [yellow]Decrypting results...[/yellow]")
    sum_result = fhe.decrypt(enc_sum)[0]
    mean_result = fhe.decrypt(enc_mean)[0]
    
    # Display results
    table = Table(title="📈 Encrypted Statistics Results", show_header=True)
    table.add_column("Metric", style="cyan")
    table.add_column("Encrypted Result", style="green")
    table.add_column("Expected", style="yellow")
    table.add_column("Match", style="magenta")
    
    expected_sum = sum(complexity_scores)
    expected_mean = expected_sum / len(complexity_scores)
    
    sum_match = "✅" if abs(sum_result - expected_sum) < 0.1 else "❌"
    mean_match = "✅" if abs(mean_result - expected_mean) < 0.1 else "❌"
    
    table.add_row("Sum", f"{sum_result:.2f}", f"{expected_sum:.2f}", sum_match)
    table.add_row("Mean", f"{mean_result:.2f}", f"{expected_mean:.2f}", mean_match)
    
    console.print()
    console.print(table)
    console.print()
    
    console.print("[bold green]✅ Success![/bold green]")
    console.print("[dim]All computations were done on ENCRYPTED data![/dim]\n")


def demo_encrypted_comparison():
    """
    Demonstrate comparing encrypted values.
    """
    console.print("\n[bold blue]🔬 Encrypted Comparison Demo[/bold blue]\n")
    
    # Initialize FHE
    fhe = FHEEngine()
    if not fhe.load_context():
        fhe.setup(scheme="ckks")
    
    # Two datasets
    team_a_productivity = [85.5, 92.3, 78.9, 88.7, 91.2]
    team_b_productivity = [82.1, 89.4, 91.8, 85.3, 88.9]
    
    console.print(f"📊 Team A Productivity: {team_a_productivity}")
    console.print(f"📊 Team B Productivity: {team_b_productivity}\n")
    
    # Encrypt
    console.print("🔐 Encrypting data...")
    enc_a = fhe.encrypt(team_a_productivity)
    enc_b = fhe.encrypt(team_b_productivity)
    console.print("✅ Data encrypted\n")
    
    # Compute means on encrypted data
    console.print("🔬 Computing means (encrypted)...")
    enc_mean_a = fhe.mean_encrypted(enc_a)
    enc_mean_b = fhe.mean_encrypted(enc_b)
    
    # Decrypt
    console.print("🔓 Decrypting results...")
    mean_a = fhe.decrypt(enc_mean_a)[0]
    mean_b = fhe.decrypt(enc_mean_b)[0]
    
    # Display
    console.print(f"\n[cyan]Team A Average:[/cyan] {mean_a:.2f}")
    console.print(f"[cyan]Team B Average:[/cyan] {mean_b:.2f}")
    
    winner = "Team A" if mean_a > mean_b else "Team B"
    console.print(f"\n[green]🏆 Winner: {winner}[/green]\n")
    
    console.print("[dim]Comparison done on encrypted data![/dim]\n")


def demo_polynomial_evaluation():
    """
    Demonstrate polynomial evaluation on encrypted data.
    Example: f(x) = 2x^2 + 3x + 1
    """
    console.print("\n[bold blue]🔬 Encrypted Polynomial Evaluation[/bold blue]\n")
    
    # Initialize FHE
    fhe = FHEEngine()
    if not fhe.load_context():
        fhe.setup(scheme="ckks")
    
    # Data and polynomial
    x_values = [1.0, 2.0, 3.0, 4.0, 5.0]
    coefficients = [1, 3, 2]  # 1 + 3x + 2x^2
    
    console.print(f"📊 Input values (x): {x_values}")
    console.print(f"📐 Polynomial: f(x) = {coefficients[0]} + {coefficients[1]}x + {coefficients[2]}x²\n")
    
    # Encrypt
    console.print("🔐 Encrypting data...")
    enc_x = fhe.encrypt(x_values)
    console.print("✅ Data encrypted\n")
    
    # Evaluate polynomial on encrypted data
    console.print("🔬 Evaluating polynomial (encrypted)...")
    enc_result = fhe.polynomial_eval_encrypted(enc_x, coefficients)
    
    # Decrypt
    console.print("🔓 Decrypting results...")
    result = fhe.decrypt(enc_result)[:len(x_values)]
    
    # Expected values
    expected = [coefficients[0] + coefficients[1]*x + coefficients[2]*x**2 for x in x_values]
    
    # Display
    table = Table(title="Polynomial Evaluation Results")
    table.add_column("x", style="cyan")
    table.add_column("f(x) Encrypted", style="green")
    table.add_column("f(x) Expected", style="yellow")
    
    for x, enc_val, exp_val in zip(x_values, result, expected):
        table.add_row(f"{x:.1f}", f"{enc_val:.2f}", f"{exp_val:.2f}")
    
    console.print()
    console.print(table)
    console.print()
    
    console.print("[bold green]✅ Polynomial evaluated on encrypted data![/bold green]\n")


def main():
    """Run all demos."""
    console.print("\n" + "="*60)
    console.print("[bold cyan]🎯 FHE Computation Examples[/bold cyan]")
    console.print("="*60 + "\n")
    
    demos = [
        ("Statistics on Encrypted Data", demo_encrypted_statistics),
        ("Encrypted Comparison", demo_encrypted_comparison),
        ("Polynomial Evaluation", demo_polynomial_evaluation)
    ]
    
    for i, (name, demo_func) in enumerate(demos, 1):
        console.print(f"\n[bold yellow]Demo {i}: {name}[/bold yellow]")
        console.print("-" * 60)
        demo_func()
        
        if i < len(demos):
            console.print("\n[dim]Press Enter for next demo...[/dim]")
            input()
    
    console.print("\n[bold green]✅ All demos complete![/bold green]\n")


if __name__ == "__main__":
    main()
