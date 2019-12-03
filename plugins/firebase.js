import firebase from 'firebase'

const firebaseConfig = {
  apiKey: 'key',
  authDomain: 'project-id.firebaseapp.com',
  databaseURL: 'https:/project-id.firebaseio.com',
  projectId: 'project-id',
  storageBucket: 'project-id.appspot.com',
  messagingSenderId: 'sender-id',
  appId: 'app-id',
  measurementId: 'G-measurement-id'
}

const app = firebase.initializeApp(firebaseConfig)

export const db = app.database
