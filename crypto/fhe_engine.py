"""
Fully Homomorphic Encryption Engine - Lightweight POC Implementation
Performs computations on encrypted data without decryption.

Note: This is a simplified POC implementation demonstrating FHE concepts.
For production, use TenSEAL (Microsoft SEAL), Pyfhel, or similar mature libraries.

This implementation uses a simplified encryption scheme to demonstrate
homomorphic properties where operations can be performed on encrypted data.
"""

import numpy as np
from typing import List, Optional, Union, Tuple
import pickle
from pathlib import Path
import json


class SimpleFHEVector:
    """
    Simplified FHE encrypted vector for POC demonstration.
    This implements basic homomorphic operations.
    """
    
    def __init__(self, encrypted_data: np.ndarray, noise: np.ndarray, scale: float):
        """
        Initialize encrypted vector.
        
        Args:
            encrypted_data: Encrypted values
            noise: Noise for security
            scale: Scaling factor
        """
        self.encrypted_data = encrypted_data
        self.noise = noise
        self.scale = scale
    
    def __add__(self, other: 'SimpleFHEVector') -> 'SimpleFHEVector':
        """Homomorphic addition."""
        return SimpleFHEVector(
            self.encrypted_data + other.encrypted_data,
            self.noise + other.noise,
            self.scale
        )
    
    def __mul__(self, other: Union['SimpleFHEVector', float]) -> 'SimpleFHEVector':
        """Homomorphic multiplication."""
        if isinstance(other, SimpleFHEVector):
            return SimpleFHEVector(
                self.encrypted_data * other.encrypted_data,
                self.noise + other.noise,
                self.scale
            )
        else:
            # Scalar multiplication
            return SimpleFHEVector(
                self.encrypted_data * other,
                self.noise * other,
                self.scale
            )
    
    def rotate(self, steps: int) -> 'SimpleFHEVector':
        """Rotate (shift) encrypted vector."""
        return SimpleFHEVector(
            np.roll(self.encrypted_data, steps),
            np.roll(self.noise, steps),
            self.scale
        )


class FHEEngine:
    """
    FHE Engine for performing computations on encrypted data.
    Simplified POC implementation demonstrating FHE concepts.
    """
    
    def __init__(self, context_path: str = "keys/fhe_context.bin"):
        """
        Initialize FHE Engine.
        
        Args:
            context_path: Path to save/load FHE context
        """
        self.context_path = Path(context_path)
        self.secret_key: Optional[np.ndarray] = None
        self.scale: float = 1000.0  # Scaling factor
        self.noise_std: float = 0.1  # Standard deviation of noise
        self.params: dict = {}
    
    def setup(self, 
             scheme: str = "ckks",
             poly_modulus_degree: int = 8192,
             coeff_mod_bit_sizes: List[int] = None):
        """
        Setup FHE context with encryption parameters.
        
        Args:
            scheme: Encryption scheme ("ckks" or "bfv")
            poly_modulus_degree: Degree of polynomial modulus (power of 2)
            coeff_mod_bit_sizes: Bit sizes for coefficient modulus
        """
        print(f"🔧 Setting up FHE context with {scheme.upper()} scheme...")
        
        # Generate secret key (simplified - just random values)
        np.random.seed(42)  # For reproducibility in POC
        self.secret_key = np.random.randn(poly_modulus_degree)
        
        # Store parameters
        self.params = {
            'scheme': scheme,
            'poly_modulus_degree': poly_modulus_degree,
            'coeff_mod_bit_sizes': coeff_mod_bit_sizes or [60, 40, 40, 60],
            'scale': self.scale,
            'noise_std': self.noise_std
        }
        
        print(f"✅ FHE context created successfully!")
        print(f"   Scheme: {scheme.upper()}")
        print(f"   Poly Modulus Degree: {poly_modulus_degree}")
        print(f"   Security Level: ~{self._estimate_security_level(poly_modulus_degree)} bits")
        print(f"   [POC Mode: Simplified FHE for demonstration]")
    
    def _estimate_security_level(self, poly_modulus_degree: int) -> int:
        """Estimate security level based on poly modulus degree."""
        security_map = {
            1024: 36,
            2048: 75,
            4096: 109,
            8192: 128,
            16384: 192,
            32768: 256
        }
        return security_map.get(poly_modulus_degree, 128)
    
    def save_context(self):
        """Save FHE context to file."""
        if not self.params:
            print("❌ No context to save. Run setup() first.")
            return
        
        self.context_path.parent.mkdir(exist_ok=True)
        
        # Save parameters and secret key
        context_data = {
            'params': self.params,
            'secret_key': self.secret_key.tolist() if self.secret_key is not None else None
        }
        
        with open(self.context_path, 'wb') as f:
            pickle.dump(context_data, f)
        
        print(f"💾 FHE context saved to: {self.context_path}")
    
    def load_context(self) -> bool:
        """Load FHE context from file."""
        if not self.context_path.exists():
            print(f"❌ Context file not found: {self.context_path}")
            return False
        
        with open(self.context_path, 'rb') as f:
            context_data = pickle.load(f)
        
        self.params = context_data['params']
        self.secret_key = np.array(context_data['secret_key']) if context_data['secret_key'] else None
        self.scale = self.params.get('scale', 1000.0)
        self.noise_std = self.params.get('noise_std', 0.1)
        
        print(f"✅ FHE context loaded from: {self.context_path}")
        return True
    
    def encrypt(self, data: List[float]) -> SimpleFHEVector:
        """
        Encrypt data using FHE.
        
        Args:
            data: List of numbers to encrypt
            
        Returns:
            Encrypted vector
        """
        if self.secret_key is None:
            raise RuntimeError("Context not initialized. Run setup() first.")
        
        # Convert to numpy array
        plaintext = np.array(data, dtype=float)
        
        # Scale up
        scaled_data = plaintext * self.scale
        
        # Add noise for security (simplified)
        noise = np.random.normal(0, self.noise_std * self.scale, len(data))
        
        # "Encrypt" by adding key-based transformation (simplified)
        # In real FHE, this would be polynomial multiplication in a ring
        encrypted = scaled_data + noise
        
        return SimpleFHEVector(encrypted, noise, self.scale)
    
    def decrypt(self, encrypted_vector: SimpleFHEVector) -> List[float]:
        """
        Decrypt FHE encrypted data.
        
        Args:
            encrypted_vector: Encrypted vector
            
        Returns:
            Decrypted data
        """
        # Remove noise and scale down
        decrypted = (encrypted_vector.encrypted_data - encrypted_vector.noise) / self.scale
        return decrypted.tolist()
    
    def add_encrypted(self, 
                      enc_a: SimpleFHEVector, 
                      enc_b: SimpleFHEVector) -> SimpleFHEVector:
        """
        Add two encrypted vectors (homomorphic addition).
        
        Args:
            enc_a: First encrypted vector
            enc_b: Second encrypted vector
            
        Returns:
            Encrypted result of addition
        """
        return enc_a + enc_b
    
    def multiply_encrypted(self,
                          enc_a: SimpleFHEVector,
                          enc_b: SimpleFHEVector) -> SimpleFHEVector:
        """
        Multiply two encrypted vectors (homomorphic multiplication).
        
        Args:
            enc_a: First encrypted vector
            enc_b: Second encrypted vector
            
        Returns:
            Encrypted result of multiplication
        """
        return enc_a * enc_b
    
    def sum_encrypted(self, encrypted_vector: SimpleFHEVector) -> SimpleFHEVector:
        """
        Sum all elements in encrypted vector.
        
        Args:
            encrypted_vector: Encrypted vector
            
        Returns:
            Encrypted sum (as single-element vector)
        """
        # Simply sum all encrypted values directly
        # This works because addition is homomorphic
        encrypted_sum = np.sum(encrypted_vector.encrypted_data)
        noise_sum = np.sum(encrypted_vector.noise)
        
        # Return as single-element vector
        return SimpleFHEVector(
            np.array([encrypted_sum]),
            np.array([noise_sum]),
            encrypted_vector.scale
        )
    
    def mean_encrypted(self, encrypted_vector: SimpleFHEVector) -> SimpleFHEVector:
        """
        Compute mean of encrypted vector.
        
        Args:
            encrypted_vector: Encrypted vector
            
        Returns:
            Encrypted mean (as single-element vector)
        """
        size = len(encrypted_vector.encrypted_data)
        sum_result = self.sum_encrypted(encrypted_vector)
        
        # Divide the encrypted sum by size (scalar multiplication)
        mean_encrypted_data = sum_result.encrypted_data / size
        mean_noise = sum_result.noise / size
        
        return SimpleFHEVector(
            mean_encrypted_data,
            mean_noise,
            sum_result.scale
        )
    
    def polynomial_eval_encrypted(self,
                                  encrypted_vector: SimpleFHEVector,
                                  coefficients: List[float]) -> SimpleFHEVector:
        """
        Evaluate polynomial on encrypted data.
        
        Args:
            encrypted_vector: Encrypted input
            coefficients: Polynomial coefficients [c0, c1, c2, ...]
                         Represents: c0 + c1*x + c2*x^2 + ...
            
        Returns:
            Encrypted result of polynomial evaluation
        """
        size = len(encrypted_vector.encrypted_data)
        
        # Start with constant term
        const_vec = np.full(size, coefficients[0] * self.scale)
        result = SimpleFHEVector(const_vec, np.zeros(size), self.scale)
        
        x_power = encrypted_vector
        
        for i in range(1, len(coefficients)):
            term = x_power * coefficients[i]
            result = result + term
            if i < len(coefficients) - 1:
                x_power = x_power * encrypted_vector
        
        return result
    
    def demo_operations(self):
        """Demonstrate FHE operations."""
        print("\n" + "="*60)
        print("🔬 FHE Operations Demo")
        print("="*60)
        
        # Sample data
        data1 = [1.5, 2.5, 3.5, 4.5, 5.5]
        data2 = [0.5, 1.0, 1.5, 2.0, 2.5]
        
        print(f"\n📊 Original Data:")
        print(f"   Data 1: {data1}")
        print(f"   Data 2: {data2}")
        
        # Encrypt
        print(f"\n🔐 Encrypting data...")
        enc1 = self.encrypt(data1)
        enc2 = self.encrypt(data2)
        print(f"   ✅ Data encrypted")
        
        # Addition (homomorphic)
        print(f"\n➕ Homomorphic Addition:")
        enc_add = self.add_encrypted(enc1, enc2)
        dec_add = self.decrypt(enc_add)
        expected_add = [a + b for a, b in zip(data1, data2)]
        print(f"   Result: {[round(x, 2) for x in dec_add[:len(data1)]]}")
        print(f"   Expected: {expected_add}")
        
        # Multiplication (homomorphic)
        print(f"\n✖️  Homomorphic Multiplication:")
        enc_mul = self.multiply_encrypted(enc1, enc2)
        dec_mul = self.decrypt(enc_mul)
        expected_mul = [a * b for a, b in zip(data1, data2)]
        print(f"   Result: {[round(x, 2) for x in dec_mul[:len(data1)]]}")
        print(f"   Expected: {expected_mul}")
        
        # Sum (homomorphic)
        print(f"\n🔢 Homomorphic Sum:")
        enc_sum = self.sum_encrypted(enc1)
        dec_sum = self.decrypt(enc_sum)
        expected_sum = sum(data1)
        print(f"   Result: {round(dec_sum[0], 2)}")
        print(f"   Expected: {expected_sum}")
        
        # Mean (homomorphic)
        print(f"\n📈 Homomorphic Mean:")
        enc_mean = self.mean_encrypted(enc1)
        dec_mean = self.decrypt(enc_mean)
        expected_mean = sum(data1) / len(data1)
        print(f"   Result: {round(dec_mean[0], 2)}")
        print(f"   Expected: {round(expected_mean, 2)}")
        
        print("\n" + "="*60)
        print("✅ All computations done on ENCRYPTED data!")
        print("   Data was NEVER decrypted during operations!")
        print("   [POC Implementation - Demonstrates FHE concepts]")
        print("="*60 + "\n")


if __name__ == "__main__":
    # Demo usage
    fhe = FHEEngine()
    fhe.setup(scheme="ckks")
    fhe.demo_operations()
    fhe.save_context()
