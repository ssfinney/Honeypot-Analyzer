class LogsController < ApplicationController

  # This authenticates the user through devise.
  # This is disabled since it blocks external POST requests
  # to this controller, and we need that for our python backend code.

  # Thus, we will not authenticate here until our security planning
  # is complete (probably another semester).
  # before_filter :authenticate_user!
	
  # GET /users/<id>/logs
  # GET /users/<id>/logs.json
  def index
    @logs = Log.where(user_id: params[:user_id])

    respond_to do |format|
      format.html
      format.json { render json: @logs }
    end
  end

  
  # GET /users/<id>/logs/<id>
  # GET /users/<id>/logs/<id>.json
  def show
    @log = Log.find(params[:id])

    respond_to do |format|
      format.html # show.html.erb
      format.json { render json: LogDatatable.new(view_context) }
    end
  end

  # GET /users/<id>/logs/new
  # GET /users/<id>/logs/new.json
  def new
    @log = Log.new
  end

  # POST /users/<id>/logs
  # POST /users/<id>/logs.json
  def create
    if Log.where(name: params[:name]).empty?
      @user = User.where(email: params[:user_email]).take
      @log = Log.new(name: params[:name],
		     user_id: @user.id)

      if @log.save
        respond_to do |format|
          format.html { redirect_to logs_url }
	  format.json { head :ok }
        end
      end

    else
      respond_to do |format|
        format.html { redirect_to logs_url }
	format.json { head :ok }
      end
    end
  end

  def log_params
    params.require(:log).permit(:name)
  end

  # DELETE /users/<id>/logs/<id>
  # DELETE /users/<id>/logs/<id>.json
  def destroy
    @log = Log.find(params[:id])
    @log.destroy

    respond_to do |format|
      format.html { redirect_to logs_url }
      format.json { head :ok }
    end
  end

end

