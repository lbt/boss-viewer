# This is the control file for boss-viewer.
#
# It is a configuration of ruote-kit that doesn't
# spawn a worker thread and runs inside rack

# load json backend
require 'yajl'    # fastest, but uses a c module
# require 'json_pure'  # should work everywhere

require 'ruote-kit'
require 'ruote/storage/fs_storage'

# Load config from boss config areas
boss_route_db=ENV['SERVER_DATABASE']

# Use the correct store type
store = Ruote::FsStorage.new(boss_route_db)

# establish the RuoteKit engine
RuoteKit.engine = Ruote::Engine.new(store)

# The catchall is required and must occupy the bottom position.
RuoteKit.engine.register do
  catchall
end

use Rack::CommonLogger
use Rack::Lint

run RuoteKit::Application


##################
# Local Variables:
# mode: Ruby;
# End:
