class EntriesController < ApplicationController
  # We're disabling authentication for now.
  # See the log_controller for more details.
  # before_filter :authenticate_user!

  def index
    @entries = Entry.all
  end

  def new
    @log = Log.find(params[:log_id])
    @entry = Entry.new

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @entry }
    end
  end

  def create
    @log = Log.find(params[:log_id])
    @entry = @log.entries.new(params[:entry])

    respond_to do |format|
      if @entry.save
        format.html { redirect_to @entry, notice: 'Log entry was successfully created.' }
        format.json { render json: @entry, status: :created }
      else
        format.html { render action: "new" }
        format.json { render json: @entry.errors, status: :unprocessable_entity }
      end
    end
  end

  # POST: /users/<id>/logs/<id>/entries/create_many
  def create_many
    @user = User.where(email: params[:user_email]).take
    @log = Log.where(name: params[:log_name],
		     user_id: @user.id).take

    entries = []
    params[:entries].size.times do |i|
      @entry = Entry.new(params[:entries][i])
      @entry.log_id = @log.id
      entries << @entry #Entry.new(params[:entries][i], log_id: @log.id)
    end

    if Entry.import entries
        respond_to do |format|
          format.html { redirect_to logs_url }
	  format.json { head :ok }
        end
    end
  end

  def show
    @entry = Entry.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: @entry }
    end
  end

end

