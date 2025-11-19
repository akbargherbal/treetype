import {
  GoogleAuthProvider,
  signInWithPopup,
  signOut,
  onAuthStateChanged,
  User
} from "firebase/auth";
import { auth } from "./firebase";

export class AuthManager {
  private user: User | null = null;
  private onAuthChangeCallback: ((user: User | null) => void) | null = null;

  constructor(onAuthChange?: (user: User | null) => void) {
    this.onAuthChangeCallback = onAuthChange || null;

    // Listen for auth state changes
    onAuthStateChanged(auth, (user) => {
      this.user = user;
      if (this.onAuthChangeCallback) {
        this.onAuthChangeCallback(user);
      }
    });
  }

  async signInWithGoogle(): Promise<void> {
    const provider = new GoogleAuthProvider();
    try {
      await signInWithPopup(auth, provider);
    } catch (error) {
      console.error("Error signing in with Google:", error);
      throw error;
    }
  }

  async logout(): Promise<void> {
    try {
      await signOut(auth);
    } catch (error) {
      console.error("Error signing out:", error);
      throw error;
    }
  }

  getUser(): User | null {
    return this.user;
  }

  isAuthenticated(): boolean {
    return !!this.user;
  }
}