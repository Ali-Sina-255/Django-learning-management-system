import {create} from 'zustand'
import { mountStoreDevtool } from 'simple-zustand-devtools';
const userAuthStore = create((set, get) => ({
  allUserDate: null,
  loading: false,

  // creating function in zustand
  use: () => ({
    user_id: get().allUserDate?.user_id || null,
    username: get().allUserDate?.username || null,
    full_name: get().allUserDate?.full_name || null,
  }),

  setUser: (user) =>
    set({
      allUserDate: user,
    }),
  setLoading: (loading) => set({ loading }),
  isLoggedIn: () => get().allUserDate !== null,
}));

if(import.meta.env.DEV){
    mountStoreDevtool('Store',userAuthStore);

}
export {userAuthStore}