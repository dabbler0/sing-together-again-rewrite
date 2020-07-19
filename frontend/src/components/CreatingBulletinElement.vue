<template>
      <v-form>
        <div class="text-left">
          <v-dialog width="500" v-model="dialogShown">
            <template v-slot:activator="{ on, attrs }">
              <v-btn
                color="blue lighten-2"
                dark
                v-bind="attrs"
                v-on="on"
              >
                Select Song
              </v-btn>

            </template>
            <v-card>
              <v-card-title
                class="headline grey lighten-2"
                primary-title
                >
                Select a Song
              </v-card-title>

                <v-card-text>
                  <v-list>
                    <v-list-item-group v-model="value.song" v-on:change="dialogShown=false">
                      <v-list-item
                        :key="-1"
                        :value="-1">
                        <v-list-item-content>
                          <v-list-item-title>No song</v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                      <v-list-item
                        v-for="song in songs"
                        :key="song.id"
                        :value="song.id">
                        <v-list-item-content>
                          <v-list-item-title v-text="song.name + ' (' + song.id + ')'"></v-list-item-title>
                        </v-list-item-content>
                      </v-list-item>
                    </v-list-item-group>
                  </v-list>
                </v-card-text>

                <v-divider></v-divider>

                <v-card-actions class="justify-center">
                  <v-btn v-on:click="dialogShown=false">Cancel</v-btn>

                  <v-dialog width="500" model="uploadShown">
                    <template v-slot:activator="{ on, attrs }">
                      <v-btn
                        v-bind="attrs"
                        v-on="on"
                      >
                        Upload New
                      </v-btn>

                    </template>

                    <Upload
                      v-on:cancel="uploadShown=false"
                      v-on:submit="finishUpload()"
                      :context="context"></Upload>
                  </v-dialog>

                </v-card-actions>
            </v-card>

          </v-dialog>
          <span v-if="value.song!==-1">
            Song: {{songDict[value.song].name}} ({{value.song}})
          </span>
          <span v-if="value.song===-1">
          No song
          </span>
        </div>
          <v-text-field
            v-model="value.title"
            label="Section Title"
            name="Section Title"
            type="text"
            ></v-text-field>
          <v-textarea
            v-model="value.description"
            label="Additional text for this section"
            name="Additional text for this section"
            type="text"></v-textarea>
          <v-divider class="pb-5"></v-divider>

      </v-form>
</template>

<script>
import Upload from '@/components/Upload'

export default {
  name: 'CreatingBulletinElement',
  props: ['value', 'songs', 'context'],
  watch: {
    value () {
      this.$emit('input', this.value)
    }
  },
  components: {Upload},
  data () {
    return {
      'dialogShown': false,
      'uploadShown': false,
      'songDict': {}
    }
  },
  methods: {
    finishUpload () {
      console.log('finishing upload now')
      this.uploadShown = false
      this.$emit('upload')
    }
  },
  created () {
    this.songs.forEach((song) => {
      this.songDict[song.id] = song
    })
  }
}
</script>

<!-- Add "scoped" attribute to limit CSS to this component only -->
<style scoped>
</style>
