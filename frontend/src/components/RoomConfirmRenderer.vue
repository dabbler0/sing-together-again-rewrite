<template>
  <v-card>
    <v-card-title class="headline">Look right?</v-card-title>

    <v-card-text>
      <div>
        <b>Room name:</b> {{room.title}}
      </div>

      <div>
        <b>Password:</b>
        <span v-if="room.password.length > 0">
          Yes
        </span>
        <span v-if="room.password.length == 0">
          No
        </span>
      </div>

      <div>
        <b>Expires:</b> {{room.expiration}}
      </div>

      <b>Bulletin:</b>
      <v-list disabled>
        <v-list-item
          v-for="(item, i) in room.bulletin"
          :key="i"
          >
          <v-list-item-content>
            <v-list-item-title> {{(i + 1)}}. {{item.title}} ({{(item.accompaniment ? item.accompaniment.name : 'No accompaniment')}})</v-list-item-title>
            <div class="justify-left">{{item.description}}</div>
          </v-list-item-content>
        </v-list-item>
      </v-list>
    </v-card-text>

    <v-card-actions class="justify-center">
      <v-btn @click="$emit('cancel')">Cancel</v-btn> <v-btn color="primary" @click="$emit('finish')">Finish</v-btn>
    </v-card-actions>

  </v-card>
</template>

<script>
export default {
  props: ['room'],
  data () {
    return {
    }
  }
}
</script>
