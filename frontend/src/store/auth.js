import { create } from "zustand";
import { devtools } from "zustand/middleware";

const useAuthStore = create(
  devtools((set, get) => ({
    allUserData: null,
    loading: false,

    getUserData: () => ({
      user_id: get().allUserData?.user_id || null,
      username: get().allUserData?.username || null,
    }),

    // Action to set user data
    setUser: (user) => set({ allUserData: user }),

    // Action to set loading state
    setLoading: (loading) => set({ loading }),

    // Check if the user is logged in
    isLoggedIn: () => get().allUserData !== null,
  }))
);

// Enable Zustand DevTools if in development mode
if (import.meta.env.DEV) {
  // This automatically connects to the Redux DevTools browser extension.
  useAuthStore.subscribe((state) => console.log(state)); // Optional logging
}

export { useAuthStore };
