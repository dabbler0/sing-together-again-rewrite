<template>
<v-container class="fill-height overflow-y-auto">
  <v-navigation-drawer
    v-model="drawer"
    app
    >
    <v-list dense>
      <v-list-item link @click="viewing='roominfo'">
        <v-list-item-action>
          <v-icon>mdi-cog</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          Room Info
        </v-list-item-content>
      </v-list-item>

      <v-list-item link @click="viewing='order'">
        <v-list-item-action>
          <v-icon>mdi-format-list-numbered</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          Order of Service
        </v-list-item-content>
      </v-list-item>

      <v-list-item link @click="viewing='accompaniments'">
        <v-list-item-action>
          <v-icon>mdi-music-note-plus</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          Accompaniments
        </v-list-item-content>
      </v-list-item>

      <v-list-item link @click.stop="cancelConfirmShown = true">
        <v-list-item-action>
          <v-icon>mdi-delete</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          Discard
        </v-list-item-content>
      </v-list-item>

      <v-list-item link @click.stop="finishConfirmShown = true">
        <v-list-item-action>
          <v-icon>mdi-publish</v-icon>
        </v-list-item-action>
        <v-list-item-content>
          Finish
        </v-list-item-content>
      </v-list-item>
    </v-list>
  </v-navigation-drawer>

  <v-dialog
    v-model="cancelConfirmShown"
    max-width="500"
    >

    <v-card>
      <v-card-title class="headline">Discard?</v-card-title>

      <v-card-text>This will throw away your work on this room.</v-card-text>

      <v-card-actions class="justify-center">
        <v-btn @click="cancelConfirmShown = false">Never mind</v-btn> <v-btn to="/" color="danger">Discard</v-btn>
      </v-card-actions>

    </v-card>
  </v-dialog>

  <v-dialog
    v-model="finishConfirmShown"
    max-width=500
    >
    <RoomConfirmRenderer
      :room="room"
      @cancel="finishConfirmShown=false"
      @finish="finish()"
    ></RoomConfirmRenderer>
  </v-dialog>

  <v-app-bar app color="indigo" dark>
      <v-app-bar-nav-icon @click.stop="drawer = !drawer"></v-app-bar-nav-icon>
      <v-toolbar-title>Create Room</v-toolbar-title>
  </v-app-bar>

  <!-- Room info -->
  <v-container
    fluid
    v-if="viewing=='roominfo'"
  >
    <h1>Room Info</h1>

    <v-container>
      <v-form>
        <v-text-field label="Name" v-model="room.title"></v-text-field>
        <v-text-field label="Password (optional)" v-model="room.password" type="password"></v-text-field>
        <v-menu
          ref="menu"
          :close-on-content-click="false"
          transition="scale-transition"
          offset-y
          min-width="290px"
          >
          <template v-slot:activator="{ on, attrs }">
            <v-text-field
              v-model="room.expiration"
              label="Expires after date"
              prepend-icon="event"
              readonly
              v-bind="attrs"
              v-on="on"
              ></v-text-field>
          </template>
          <v-date-picker v-model="room.expiration" no-title scrollable>
            <v-spacer></v-spacer>
            <v-btn text color="primary" @click="menu = false">Cancel</v-btn>
            <v-btn text color="primary" @click="$refs.menu.save(date)">OK</v-btn>
          </v-date-picker>
        </v-menu>

      </v-form>
    </v-container>

  </v-container>

  <v-container
    class="fill-height"
    fluid
    v-if="viewing=='order'"
  >
  <v-row>
    <v-col>
      <h1>Create the Order of Service</h1>

      <CreatingBulletinElement
          v-for="(item, i) in room.bulletin"
          style="width:100%"
          :key="i"
          v-model="room.bulletin[i]"></CreatingBulletinElement>

      <v-btn v-on:click="addSection()" large>Add section</v-btn>

    </v-col>
  </v-row>
  </v-container>

  <AccompanimentMaker
    :context="context"
    v-if="viewing=='accompaniments'"></AccompanimentMaker>

</v-container>
</template>

<script>
import CreatingBulletinElement from '@/components/CreatingBulletinElement'
import AccompanimentMaker from '@/components/AccompanimentMaker'
import RoomConfirmRenderer from '@/components/RoomConfirmRenderer'
// import brq from '@/binaryRequests'
// import encoding from '@/encoding'

export default {
  name: 'Sing',
  props: ['context'],
  components: {
    CreatingBulletinElement,
    AccompanimentMaker,
    RoomConfirmRenderer
  },
  data () {
    return { // TODO rescope to their own component
      date: '',
      viewing: 'roominfo',
      drawer: true,
      canCreate: false,

      room: {
        bulletin: [],
        expiration: (new Date()).toISOString().substring(0, 10),
        title: '',
        password: ''
      },

      finishConfirmShown: false,
      cancelConfirmShown: false
    }
  },
  methods: {
    addSection () {
      this.room.bulletin.push({
        'title': '',
        'accompaniment': null,
        'description': ''
      })
    }
  }
}
</script>

<style scoped>
</style>
